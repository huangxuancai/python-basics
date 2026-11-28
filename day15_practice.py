"""day15_practice.py —— W4 Day3：Cookie / Session / Token 本地认证靶场

对应执行卡: find-job/02-学习内容/W4/26-W4Day3-Cookie-Session-Token.md 第 5 节
运行: python day15_practice.py
特点: 纯标准库起本地服务，8 步演示三种认证机制 + JWT 无法主动失效的漏洞
产出: 控制台报告 + session_token_drill.txt
"""

import base64
import hashlib
import hmac
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import requests

sys.stdout.reconfigure(encoding="utf-8")

PORT = 8766
SECRET = b"demo-secret-key-not-for-production"  # JWT 签名密钥（真实项目放环境变量）
JWT_TTL = 3600

# ── 内存里的"用户表"和"会话表" ──
USERS = {"admin": {"pwd": "Passw0rd", "uid": 1, "role": "user"}}
SESSIONS = {}  # sid -> {"uid":1, "user":"admin", "role":"user"}


# ══════════════════════════════════════════════════════
# JWT 三件事：base64url 编码、签名、验签（不依赖任何库）
# ══════════════════════════════════════════════════════
def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64url_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)


def sign(data: bytes) -> str:
    return b64url(hmac.new(SECRET, data, hashlib.sha256).digest())


def issue_jwt(uid: int, user: str, role: str, ttl: int = JWT_TTL) -> str:
    """签发 JWT：header.payload.signature"""
    header = b64url(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    payload = b64url(json.dumps(
        {"uid": uid, "user": user, "role": role, "exp": int(time.time()) + ttl},
        separators=(",", ":"), ensure_ascii=False,
    ).encode())
    return f"{header}.{payload}.{sign(f'{header}.{payload}'.encode())}"


def verify_jwt(token: str):
    """验签 + 查过期。返回 (ok, payload_or_reason)"""
    parts = token.split(".")
    if len(parts) != 3:
        return False, "格式错误：JWT 必须三段（header.payload.signature）"
    h, p, s = parts
    if not hmac.compare_digest(sign(f"{h}.{p}".encode()), s):
        return False, "签名不一致（payload 被改过，或不是本服务器的密钥签的）"
    try:
        payload = json.loads(b64url_decode(p))
    except Exception:
        return False, "payload 解码失败"
    if payload.get("exp", 0) < time.time():
        return False, "token 已过期"
    return True, payload


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    # ── 小工具 ──
    def _json(self, code, obj, extra_headers=None):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra_headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _cookie(self, name):
        raw = self.headers.get("Cookie", "")
        for part in raw.split(";"):
            k, _, v = part.strip().partition("=")
            if k == name:
                return v
        return None

    def _query(self):
        return {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}

    # ── 路由 ──
    def do_GET(self):
        path = urlparse(self.path).path
        q = self._query()

        # ① Cookie 基础：下发
        if path == "/pref/set":
            return self._json(200, {"ok": True, "msg": "已下发偏好 cookie"},
                              {"Set-Cookie": "theme=dark; Path=/; SameSite=Lax"})

        # ① Cookie 基础：回传
        if path == "/pref/show":
            return self._json(200, {"theme_from_cookie": self._cookie("theme")})

        # ② Session 登录
        if path == "/login":
            user, pwd = q.get("user", ""), q.get("pwd", "")
            u = USERS.get(user)
            if not u or u["pwd"] != pwd:
                return self._json(401, {"ok": False, "msg": "用户名或密码错误"})
            sid = base64.urlsafe_b64encode(hashlib.sha256(f"{user}{time.time()}".encode()).digest()).decode()[:24]
            SESSIONS[sid] = {"uid": u["uid"], "user": user, "role": u["role"]}
            return self._json(200, {"ok": True, "msg": "登录成功，会话已在服务端登记", "session_count": len(SESSIONS)},
                              {"Set-Cookie": f"SID={sid}; HttpOnly; Path=/; SameSite=Lax"})

        # ② Session 校验（查表）
        if path == "/me":
            sid = self._cookie("SID")
            if not sid or sid not in SESSIONS:
                return self._json(401, {"ok": False, "msg": "未登录或会话已失效（服务端查不到这个 sid）"})
            return self._json(200, {"ok": True, "source": "服务端会话表", "user": SESSIONS[sid]})

        # ③ 登出（服务端删会话 = 主动失效）
        if path == "/logout":
            sid = self._cookie("SID")
            removed = SESSIONS.pop(sid, None) is not None if sid else False
            return self._json(200, {"ok": True, "msg": "已登出", "server_session_deleted": removed, "session_count": len(SESSIONS)},
                              {"Set-Cookie": "SID=; Max-Age=0; Path=/"})

        # ④ JWT 登录（服务器不存任何东西）
        if path == "/jwt-login":
            user, pwd = q.get("user", ""), q.get("pwd", "")
            u = USERS.get(user)
            if not u or u["pwd"] != pwd:
                return self._json(401, {"ok": False, "msg": "用户名或密码错误"})
            return self._json(200, {"ok": True, "token": issue_jwt(u["uid"], user, u["role"]),
                                    "server_stored_sessions": len(SESSIONS)})

        # ④ JWT 校验（验签，不查表）
        if path == "/jwt-me":
            auth = self.headers.get("Authorization", "")
            if not auth.startswith("Bearer "):
                return self._json(401, {"ok": False, "msg": "缺少 Authorization: Bearer <token>"})
            ok, info = verify_jwt(auth[7:])
            if not ok:
                return self._json(401, {"ok": False, "msg": info})
            return self._json(200, {"ok": True, "source": "签名验证（没查任何表）", "payload": info})

        # ⑦ 改密码：清掉该用户所有会话（Session 可主动失效），但 token 无状态无法作废
        if path == "/change-password":
            user, new = q.get("user", ""), q.get("new", "")
            if user not in USERS:
                return self._json(404, {"ok": False, "msg": "用户不存在"})
            USERS[user]["pwd"] = new
            killed = [sid for sid, v in SESSIONS.items() if v["user"] == user]
            for sid in killed:
                SESSIONS.pop(sid, None)
            return self._json(200, {"ok": True, "msg": "密码已修改",
                                    "sessions_killed": len(killed),
                                    "note": "服务端能清会话，但已签发的 JWT 它记不住"})

        return self._json(404, {"ok": False, "msg": "资源不存在"})

    do_POST = do_GET


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    time.sleep(0.3)
    base = f"http://127.0.0.1:{PORT}"

    out = []
    add = out.append
    add("=" * 88)
    add(f"Cookie / Session / Token 认证靶场 · {base}")
    add("=" * 88)

    try:
        # ══ 第 1 步：Cookie 是什么 ══
        add("\n【第 1 步】Cookie 只是「信封」：服务器下发，客户端之后自动回传")
        add("-" * 88)
        s1 = requests.Session()
        r = s1.get(f"{base}/pref/set", timeout=5)
        add(f"> GET /pref/set")
        add(f"< {r.status_code}  Set-Cookie 原文: {r.headers.get('Set-Cookie')}")
        r = s1.get(f"{base}/pref/show", timeout=5)
        add(f"> GET /pref/show   （客户端没写任何代码，cookie 自动带上）")
        add(f"< {r.status_code}  {r.json()}")
        add("观察：Cookie 自己不会认证。它只是把数据从服务器搬到客户端，再搬回来。")

        # ══ 第 2 步：Session 登录 ══
        add("\n【第 2 步】Session：登录后服务端建会话，客户端只拿一个 sid")
        add("-" * 88)
        s2 = requests.Session()
        r = s2.get(f"{base}/login", params={"user": "admin", "pwd": "Passw0rd"}, timeout=5)
        sid = s2.cookies.get("SID")
        add(f"> GET  /login?user=admin&pwd=Passw0rd")
        add(f"< {r.status_code}  Set-Cookie: {r.headers.get('Set-Cookie')}")
        add(f"   客户端只拿到 sid = {sid}")
        add(f"   服务端登记表里有 {SESSIONS[sid] if sid in SESSIONS else '?'}")
        r = s2.get(f"{base}/me", timeout=5)
        add(f"> GET  /me   （自动带 Cookie: SID={sid}）")
        add(f"< {r.status_code}  {r.json()}")
        add("观察：服务器拿 sid 去会话表里查，查到才知道你是谁 → 这就是「有状态」。")

        # ══ 第 3 步：登出 = 服务端主动失效 ══
        add("\n【第 3 步】Session 能主动失效：登出后同一 sid 立刻失效")
        add("-" * 88)
        old_sid = sid
        r = s2.get(f"{base}/logout", timeout=5)
        add(f"> GET  /logout")
        add(f"< {r.status_code}  {r.json()}")
        s3 = requests.Session()
        s3.cookies.set("SID", old_sid)
        r = s3.get(f"{base}/me", timeout=5)
        add(f"> GET  /me   （手动把旧 sid={old_sid} 塞回 cookie，模拟盗号者）")
        add(f"< {r.status_code}  {r.json()}")
        add("观察：服务端删了那条会话，旧 sid 立刻废掉。这是 Session 的最大优势。")

        # ══ 第 4 步：JWT 登录 ══
        add("\n【第 4 步】JWT：服务器签一个自包含 token，自己不存任何东西")
        add("-" * 88)
        r = requests.get(f"{base}/jwt-login", params={"user": "admin", "pwd": "Passw0rd"}, timeout=5)
        token = r.json()["token"]
        add(f"> GET  /jwt-login?user=admin&pwd=Passw0rd")
        add(f"< {r.status_code}  token = {token[:60]}...（共 {len(token)} 字符）")
        add(f"   服务器当前会话表条数: {r.json()['server_stored_sessions']}（JWT 登录不产生会话）")
        hdr = {"Authorization": f"Bearer {token}"}
        r = requests.get(f"{base}/jwt-me", headers=hdr, timeout=5)
        add(f"> GET  /jwt-me   Authorization: Bearer <token>")
        add(f"< {r.status_code}  {r.json()}")
        add("观察：服务器没查任何表，验签就把你算出来了 → 这就是「无状态」。")

        # ══ 第 5 步：payload 是明文 ══
        add("\n【第 5 步】JWT 的 payload 用 Base64 编码，谁都能解开看")
        add("-" * 88)
        h, p, sig = token.split(".")
        decoded = json.loads(b64url_decode(p))
        add(f"   原始 payload（Base64）: {p}")
        add(f"   解码后: {json.dumps(decoded, ensure_ascii=False)}")
        add(f"   header 解码: {json.loads(b64url_decode(h))}")
        add("观察：uid / user / role / exp 全明文。Base64 是编码不是加密。")
        add("     → 推论：绝不能在 payload 里放密码、身份证号、手机号")

        # ══ 第 6 步：篡改 payload ══
        add("\n【第 6 步】篡改 payload 的 role → 签名对不上 → 401")
        add("-" * 88)
        forged_payload = dict(decoded, role="admin")
        forged_p = b64url(json.dumps(forged_payload, separators=(",", ":"), ensure_ascii=False).encode())
        forged_token = f"{h}.{forged_p}.{sig}"  # 签名沿用旧的，签名算不出来就只能这么试
        add(f"   篡改后 payload: {json.dumps(forged_payload, ensure_ascii=False)}")
        r = requests.get(f"{base}/jwt-me", headers={"Authorization": f"Bearer {forged_token}"}, timeout=5)
        add(f"< {r.status_code}  {r.json()}")
        add("观察：防篡改靠的是签名（HMAC-SHA256 + 服务器密钥），不是「看不见」。")
        add("     想自己重算签名？没有密钥算不出来。")

        # ══ 第 7 步：改密码后的生死差别 ══
        add("\n【第 7 步】⭐ 改密码后：Session 立刻失效，JWT 仍然有效（漏洞现场）")
        add("-" * 88)
        s4 = requests.Session()
        r = s4.get(f"{base}/login", params={"user": "admin", "pwd": "Passw0rd"}, timeout=5)
        sid_b = s4.cookies.get("SID")
        add(f"   先重新登录：新 sid = {sid_b}，新 token 沿用第 4 步那个")
        r = s4.get(f"{base}/me", timeout=5)
        add(f"   改密前 /me（Session）    → {r.status_code}")

        r = requests.get(f"{base}/change-password", params={"user": "admin", "new": "NewPass!2026"}, timeout=5)
        add(f"> GET  /change-password?user=admin&new=NewPass!2026")
        add(f"< {r.status_code}  {r.json()}")

        r = s4.get(f"{base}/me", timeout=5)
        add(f"   改密后 /me（Session）    → {r.status_code}  {r.json().get('msg')}")
        r = requests.get(f"{base}/jwt-me", headers=hdr, timeout=5)
        add(f"   改密后 /jwt-me（JWT）    → {r.status_code}  {r.json().get('payload')}")
        add("")
        add("   ⚠️ 同一个用户、同一次密码修改：")
        add("      Session 手里的凭证立刻作废（服务端删了会话）")
        add("      JWT 手里的旧 token 依然能访问（服务器没有作废它的手段）")
        add("   → 这就是'JWT 无法主动登出'的真实后果。工程解法：")
        add("      ① 黑名单（作废列表）② 短有效期 access + 可撤销 refresh ③ token 带密码版本号")

        # 还原密码，避免影响二次运行
        requests.get(f"{base}/change-password", params={"user": "admin", "new": "Passw0rd"}, timeout=5)

        # ══ 第 8 步：对照表 ══
        add("\n【第 8 步】三种方案对照（背这四行就够）")
        add("-" * 88)
        add(f"{'':<14}{'Cookie':<18}{'Session':<20}{'Token(JWT)'}")
        add(f"{'本质':<14}{'传输容器':<18}{'服务端会话':<20}{'自包含凭证'}")
        add(f"{'数据存哪':<14}{'客户端':<18}{'服务端':<20}{'客户端(payload)'}")
        add(f"{'状态性':<14}{'—':<18}{'有状态':<20}{'无状态'}")
        add(f"{'能否主动失效':<12}{'删 cookie':<18}{'删会话 ✅':<20}{'只能等过期 ❌'}")
        add(f"{'分布式':<14}{'—':<18}{'要共享(Redis)':<20}{'天然支持 ✅'}")
        add("\n面试三句话：")
        add("  1) HTTP 无状态，登录就是在无状态协议上造'我记得你'的假象；Cookie 是信封不是方案")
        add("  2) Session 有状态——服务端存会话，能主动失效，但要共享、占内存")
        add("  3) JWT 无状态——签名自包含，天然分布式，但无法主动失效、payload 明文可读")
    finally:
        server.shutdown()
        server.server_close()

    report = "\n".join(out)
    print(report)
    with open("session_token_drill.txt", "w", encoding="utf-8") as f:
        f.write(report + "\n")
    print("\n✅ 已存档到 session_token_drill.txt")


if __name__ == "__main__":
    main()
