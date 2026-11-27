"""day14_practice.py —— W4 Day2：HTTP 状态码本地靶场

对应执行卡: find-job/02-学习内容/W4/25-W4Day2-状态码全家桶.md 第 4 节
运行: python day14_practice.py
特点: 纯标准库起本地服务，不联网、不走代理，16 个状态码一次全触发
产出: 控制台报告 + status_code_drill.txt
"""

import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import requests

# Windows 控制台默认 GBK，中文会炸 UnicodeEncodeError（W1 的老坑）
sys.stdout.reconfigure(encoding="utf-8")

PORT = 8765
ETAG = '"v1-20261127"'

# ── 靶场路由表：路径 → (状态码, 响应体, 额外头) ──
# 这就是"服务器在什么情况下返什么码"的最小演示
ROUTES = {
    "/200": (200, {"code": 0, "msg": "ok", "data": {"user": "admin"}}, {}),
    "/201": (201, {"code": 0, "msg": "created", "id": 1001}, {"Location": "/users/1001"}),
    "/204": (204, None, {}),  # 成功但无响应体，DELETE 常用
    "/301": (301, None, {"Location": "/200"}),  # 永久搬家
    "/302": (302, None, {"Location": "/login"}),  # 临时搬家
    "/400": (400, {"code": 40000, "msg": "参数 age 必须是整数，收到 'abc'"}, {}),
    "/401": (401, {"code": 40100, "msg": "未提供有效的访问令牌"}, {}),
    "/403": (403, {"code": 40300, "msg": "无权访问该资源（该订单不属于当前用户）"}, {}),
    "/404": (404, {"code": 40400, "msg": "资源不存在"}, {}),
    "/only-post": (405, {"code": 40500, "msg": "该接口只支持 POST"}, {"Allow": "POST"}),
    "/429": (429, {"code": 42900, "msg": "请求过于频繁，请稍后再试"}, {"Retry-After": "60"}),
    "/500": (500, {"code": 50000, "msg": "NullPointerException at OrderService.java:88"}, {}),
    "/502": (502, {"code": 50200, "msg": "后端服务无响应（进程未启动或端口不通）"}, {}),
    "/503": (503, {"code": 50300, "msg": "服务维护中，暂停接收流量"}, {"Retry-After": "120"}),
    "/504": (504, {"code": 50400, "msg": "上游服务响应超时（等待 30s 未返回）"}, {}),
}

CATEGORY = {
    2: ("2xx 成功", "—"),
    3: ("3xx 重定向", "服务器指路"),
    4: ("4xx 客户端错误", "客户端（你的锅）"),
    5: ("5xx 服务端错误", "服务端（服务器的锅）"),
}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):  # 静音默认日志
        pass

    def _send(self, code, payload, extra=None):
        body = b"" if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        if payload is not None:
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        # 204/304 规范上禁止有 body，也不带 Content-Length
        if payload is None and code not in (204, 304):
            self.send_header("Content-Length", "0")
        self.end_headers()
        if body and code not in (204, 304):
            self.wfile.write(body)

    def _handle(self):
        path = self.path.split("?")[0]

        # 304 特殊逻辑：第一次给 ETag，带 If-None-Match 再来就返 304
        if path == "/304":
            if self.headers.get("If-None-Match") == ETAG:
                self._send(304, None, {"ETag": ETAG})
            else:
                self._send(200, {"code": 0, "data": "资源内容（第一次完整返回）"}, {"ETag": ETAG})
            return

        # 405 演示：只支持 POST 的接口被 GET 打
        if path == "/only-post" and self.command != "POST":
            code, payload, extra = ROUTES["/only-post"]
            self._send(code, payload, extra)
            return

        if path in ROUTES:
            code, payload, extra = ROUTES[path]
            self._send(code, payload, extra)
        else:
            self._send(404, {"code": 40400, "msg": "资源不存在"})

    do_GET = _handle
    do_POST = _handle
    do_DELETE = _handle


# ── 测试用例：方法、路径、请求体、是否跟随重定向 ──
CASES = [
    ("GET", "/200", None, True),
    ("POST", "/201", {"username": "admin"}, True),
    ("DELETE", "/204", None, True),
    ("GET", "/301", None, False),  # 不跟随，看 301 原貌
    ("GET", "/301", None, True),   # 跟随，看到最终 200
    ("GET", "/302", None, False),
    ("GET", "/304", None, True),   # 第 1 次：200 + ETag
    ("GET", "/304", None, True),   # 第 2 次：带 If-None-Match → 304
    ("POST", "/400", {"age": "abc"}, True),
    ("GET", "/401", None, True),
    ("GET", "/403", None, True),
    ("GET", "/404", None, True),
    ("GET", "/only-post", None, True),
    ("GET", "/429", None, True),
    ("GET", "/500", None, True),
    ("GET", "/502", None, True),
    ("GET", "/503", None, True),
    ("GET", "/504", None, True),
]


def call(base, method, path, payload, follow, headers=None):
    return requests.request(
        method, base + path, json=payload, timeout=5,
        allow_redirects=follow, headers=headers or {},
    )


def describe(r, follow, path=""):
    """把一次响应压成一行可读说明。"""
    bits = []
    if path in ("/301", "/302") and follow:
        return f"已自动跟随重定向 → 最终落到 {r.status_code}（requests 默认行为）"
    if r.status_code in (301, 302, 303, 307, 308):
        loc = r.headers.get("Location", "(无)")
        bits.append(f"Location={loc}，未跟随（allow_redirects=False）" if not follow else f"已自动跟随 → 最终 {r.status_code}")
    if r.status_code == 204:
        bits.append(f"body 长度={len(r.content)}（成功但无内容）")
    if r.status_code == 304:
        bits.append(f"body 长度={len(r.content)}（用本地缓存，省流量）")
    if r.status_code == 405:
        bits.append(f"Allow={r.headers.get('Allow', '(无)')}")
    if r.status_code in (429, 503):
        bits.append(f"Retry-After={r.headers.get('Retry-After', '(无)')}")
    if r.status_code >= 400:
        try:
            bits.append("服务器原话: " + r.json().get("msg", ""))
        except Exception:
            bits.append(f"body={r.text[:60]!r}")
    return "；".join(bits) if bits else "正常响应"


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    time.sleep(0.3)
    base = f"http://127.0.0.1:{PORT}"

    out = []
    add = out.append
    add("=" * 92)
    add(f"HTTP 状态码靶场 · 本地服务 {base}")
    add("=" * 92)

    results = []
    try:
        etag_cache = None
        seen_304 = 0
        for method, path, payload, follow in CASES:
            headers = {}
            note = ""
            if path == "/304":
                if seen_304 == 0:
                    note = "第1次请求（无缓存）"
                else:
                    headers["If-None-Match"] = etag_cache
                    note = "第2次请求（带 If-None-Match）"
                seen_304 += 1
            r = call(base, method, path, payload, follow, headers)
            if path == "/304" and r.status_code == 200:
                etag_cache = r.headers.get("ETag")

            results.append((method, path, r, follow, note))

        # ── 按类别分组打印 ──
        for cat in (2, 3, 4, 5):
            name, blame = CATEGORY[cat]
            rows = [x for x in results if x[2].status_code // 100 == cat]
            if not rows:
                continue
            add(f"\n【{name}】 锅在：{blame}")
            add("-" * 92)
            add(f"{'METHOD':<8}{'PATH':<13}{'CODE':<6}{'REASON':<26}{'DETAIL'}")
            for method, path, r, follow, note in rows:
                desc = describe(r, follow, path)
                if note:
                    desc = f"[{note}] " + desc
                add(f"{method:<8}{path:<13}{r.status_code:<6}{r.reason:<26}{desc}")

        # ── 三组辨析对照 ──
        add("\n" + "=" * 92)
        add("【三组易混辨析 —— 面试原题】")
        add("=" * 92)
        add("① 401 vs 403")
        add("   401 未认证：没带 token / token 过期 → 重新登录能解决")
        add("   403 无权限：身份有效但权限不够 → 重新登录也没用")
        add("   ⚠️ 越权测试：普通用户访问管理员接口若返 200+数据，是严重漏洞")
        add("\n② 301 vs 302")
        add("   301 永久：浏览器会长期缓存，发错等于事故")
        add("   302 临时：每次都会重新问服务器，登录跳转用这个")
        add("\n③ 500 vs 502 vs 503 vs 504（按链路）")
        add("   500 应用代码崩了（后端答了，答案是'我错了'）")
        add("   502 网关拿不到后端（后端不在了：进程挂/端口不通）")
        add("   503 服务暂不可用（过载保护/发布中，有 Retry-After）")
        add("   504 网关等后端超时（后端还在，只是慢）")

        # ── 自检：期望 vs 实际 ──
        add("\n" + "=" * 92)
        add("【自检】期望状态码 vs 实际（能程序化的不靠肉眼）")
        add("=" * 92)
        expected = [
            ("GET", "/200", 200), ("POST", "/201", 201), ("DELETE", "/204", 204),
            ("GET", "/301", 301), ("GET", "/301", 200), ("GET", "/302", 302),
            ("GET", "/304", 200), ("GET", "/304", 304), ("POST", "/400", 400),
            ("GET", "/401", 401), ("GET", "/403", 403), ("GET", "/404", 404),
            ("GET", "/only-post", 405), ("GET", "/429", 429), ("GET", "/500", 500),
            ("GET", "/502", 502), ("GET", "/503", 503), ("GET", "/504", 504),
        ]
        # CASES 与 expected 顺序一一对应，直接按序比对（不靠肉眼，也不靠猜）
        checks = []
        for i, (m, p, exp) in enumerate(expected):
            actual = results[i][2].status_code if i < len(results) else None
            checks.append((m, p, exp, actual))

        fails = 0
        for m, p, exp, actual in checks:
            ok = exp == actual
            fails += 0 if ok else 1
            note = " (第2次带If-None-Match)" if p == "/304" and exp == 304 else ""
            add(f"{'PASS' if ok else 'FAIL'}  {m:<7}{p:<12}期望 {exp}  实际 {actual}{note}")
        add(f"\n结果：{len(checks) - fails}/{len(checks)} PASS" + ("" if fails == 0 else f"，{fails} 项 FAIL"))

        add("\n" + "=" * 92)
        add("【附加实验】想亲眼看'越权漏洞'的报文长什么样？")
        add("=" * 92)
        add("   把上面 ROUTES 里 /403 那行改成：")
        add('   "/403": (200, {"code": 0, "data": "别人的订单：1001 元"}, {}),')
        add("   重跑本脚本 → 你会看到本该 403 的请求返回 200 + 别人的数据。")
        add("   这就是越权漏洞在协议层的样子。看完改回来。")
    finally:
        server.shutdown()
        server.server_close()

    report = "\n".join(out)
    print(report)
    with open("status_code_drill.txt", "w", encoding="utf-8") as f:
        f.write(report + "\n")
    print("\n✅ 已存档到 status_code_drill.txt")


if __name__ == "__main__":
    main()
