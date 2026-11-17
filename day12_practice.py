"""W2 Day6 练习：requests GET + 响应读取 + 安全请求（13 题）

用法：
    cd C:\\Users\\-\\Desktop\\study_Python-Basics_20251108_v1.0\\python-basics
    $env:PYTHONIOENCODING='utf-8'; venv\\Scripts\\python.exe day12_practice.py

    # 只跑某一区
    venv\\Scripts\\python.exe day12_practice.py A

讲义：02-学习内容/15-W2Day6-requests库.md

分区：
    A 区（4 题）Response 解剖      → 讲义 2-3 节
    B 区（3 题）状态码与安全请求    → 讲义 4 节
    C 区（3 题）params 与 headers  → 讲义 5 节
    D 区（3 题）timeout            → 讲义 6 节

注意：本文件会真实联网（httpbin.org / gov.cn），全程约 30 秒。
"""

import sys
import time

import requests

BIN = "https://httpbin.org"


# ─────────────────────────────────────────────────────────────
# 0 · 开场自测（先答，不看讲义）
# ─────────────────────────────────────────────────────────────

SELF_TEST = {
    "Q1": "requests.get(url) 返回的是什么类型的对象？",
    "Q2": "服务器返回 404，requests.get 会抛异常吗？",
    "Q3": "r.text 和 r.content 有什么区别？",
    "Q4": "timeout=5 限制的是「整个请求最多 5 秒」吗？",
    "Q5": "为什么抓中文网页经常乱码？",
}

MY_ANSWERS = {
    "Q1": "requests.models.Response",
    "Q2": "不会",
    "Q3": "r.text是文本，r.content是编码",
    "Q4": "不是，是连接最多等5秒+连接成功后最多等等5秒",
    "Q5": "因为requests没按UTF-8解码",
}


def q0_self_test():
    print("\n" + "=" * 60)
    print("0 · 开场自测（答案在讲义 2.1 / 4.1 / 3.2 / 6.2 / 3.3）")
    print("=" * 60)
    for k, q in SELF_TEST.items():
        print(f"  {k}. {q}")
        print(f"      我的答案: {MY_ANSWERS[k]}")


# ─────────────────────────────────────────────────────────────
# A 区（4 题）Response 解剖
# ─────────────────────────────────────────────────────────────


def a1_解剖():
    """A1 GET httpbin，打印 type / status_code / ok / elapsed。"""
    r = requests.get(BIN + "/get", timeout=10)
    print("  type        =", type(r))
    print("  status_code =", r.status_code)
    print("  ok          =", r.ok)
    print("  reason      =", r.reason)
    print("  elapsed     =", r.elapsed)
    print("  url         =", r.url)


def a2_text与content():
    """A2 打印 len(r.text) 和 len(r.content)，解释为什么可能不等。"""
    r = requests.get(BIN + "/get", timeout=10)
    print("  httpbin: len(text) =", len(r.text), "| len(content) =", len(r.content))

    r2 = requests.get("https://www.gov.cn/", timeout=15)
    r2.encoding = r2.apparent_encoding
    ratio = len(r2.content) / max(len(r2.text), 1)
    print(f"  gov.cn:  len(text) = {len(r2.text)} | len(content) = {len(r2.content)} | {ratio:.2f}x")


def _title_of(html):
    i = html.find("<title>")
    if i < 0:
        return "(没有 title)"
    j = html.find("</title>", i)
    if j < 0:
        return "(title 没闭合)"
    return html[i + 7:j].strip()


def a3_乱码修正():
    """A3 抓 gov.cn：先看 Content-Type，再打印未修正 title，再改 encoding 打印。"""
    r = requests.get("https://www.gov.cn/", timeout=15)
    ct = r.headers.get("Content-Type")
    print("  Content-Type =", ct)
    print("  requests 猜的 encoding =", r.encoding)
    print("  apparent_encoding      =", r.apparent_encoding)
    print("  未修正 title =", repr(_title_of(r.text)))
    r.encoding = r.apparent_encoding
    print("  修正后 title =", repr(_title_of(r.text)))


def a4_json解析失败():
    """A4 抓 HTML 页面调 .json()，捕获异常并打印完整类名。"""
    r = requests.get("https://www.baidu.com", timeout=15)
    print("  Content-Type =", r.headers.get("Content-Type"))
    try:
        r.json()
        print("  ⚠️ 居然成功了？")
    except Exception as e:
        print("  异常类型 =", type(e).__name__)
        print("  __module__ =", type(e).__module__)
        print("  消息 =", str(e)[:80])
        print("  是 requests 的异常吗 →", isinstance(e, requests.exceptions.RequestException))


# ─────────────────────────────────────────────────────────────
# B 区（3 题）状态码与安全请求
# ─────────────────────────────────────────────────────────────


def b1_404不抛异常():
    """B1 请求 404 和 500，证明没有抛异常。"""
    for code in (404, 500):
        try:
            r = requests.get(f"{BIN}/status/{code}", timeout=10)
            print(f"  {code}: status_code={r.status_code} | ok={r.ok} | reason={r.reason} | 没抛异常")
        except requests.exceptions.RequestException as e:
            print(f"  {code}: 抛了 {type(e).__name__}（意外！）")


def b2_raise_for_status():
    """B2 对 404 调 raise_for_status()，捕获并打印。"""
    r = requests.get(BIN + "/status/404", timeout=10)
    try:
        r.raise_for_status()
        print("  ⚠️ 没抛异常？")
    except requests.exceptions.HTTPError as e:
        print("  异常类型 =", type(e).__name__)
        print("  消息     =", str(e))
        print("  e.response.status_code =", e.response.status_code)


def b3_safe_get():
    """B3 用 safe_get 请求不存在的域名，确认给人话提示。"""

    def safe_get(url, timeout=10):
        try:
            r = requests.get(url, timeout=timeout)
            r.raise_for_status()
            return r
        except requests.exceptions.Timeout:
            raise RuntimeError(f"请求超时（{timeout} 秒），检查网络")
        except requests.exceptions.ConnectionError:
            raise RuntimeError(f"连不上 {url}，检查域名/网络/代理")
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"服务器返回 {e.response.status_code} {e.response.reason}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"请求失败: {type(e).__name__}: {e}")

    try:
        safe_get("https://no-such-host-abc123xyz.invalid/get")
    except RuntimeError as e:
        print("  人话提示 =", e)
        print("  不是 Traceback ✅")


# ─────────────────────────────────────────────────────────────
# C 区（3 题）params 与 headers
# ─────────────────────────────────────────────────────────────


def c1_params编码():
    """C1 用 params 传中文 + 列表，打印最终 url。"""
    r = requests.get(
        BIN + "/get",
        params={"q": "python 学习", "page": 2, "tag": ["a", "b"]},
        timeout=10,
    )
    print("  r.url =", r.url)
    print("  回显 args =", r.json()["args"])


def c2_改UA():
    """C2 打印默认 UA，再改成浏览器 UA 对比。"""
    r1 = requests.get(BIN + "/get", timeout=10)
    print("  默认 User-Agent =", r1.json()["headers"]["User-Agent"])

    ua = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    r2 = requests.get(BIN + "/get", headers={"User-Agent": ua}, timeout=10)
    print("  改后回显       =", r2.json()["headers"]["User-Agent"])


def c3_None值处理():
    """C3 params 里 None 和空字符串的处理。"""
    r = requests.get(BIN + "/get", params={"a": 1, "b": None, "c": ""}, timeout=10)
    print("  r.url =", r.url)
    print("  回显 args =", r.json()["args"])
    print("  b=None 消失了 ✅ | c='' 保留了 ✅")


# ─────────────────────────────────────────────────────────────
# D 区（3 题）timeout
# ─────────────────────────────────────────────────────────────


def d1_ReadTimeout():
    """D1 timeout=1 打 /delay/5，捕获异常并打印类型 + 耗时。"""
    t0 = time.time()
    try:
        requests.get(BIN + "/delay/5", timeout=1)
        print("  ⚠️ 没抛异常？")
    except Exception as e:
        dt = time.time() - t0
        print(f"  {type(e).__name__} 用时 {dt:.2f}s")
        print(f"  是 Timeout 吗 → {isinstance(e, requests.exceptions.Timeout)}")
        print(f"  是 ConnectionError 吗 → {isinstance(e, requests.exceptions.ConnectionError)}")


def d2_ConnectionError():
    """D2 打一个不存在的域名，捕获异常并打印类型 + 耗时。"""
    t0 = time.time()
    try:
        requests.get("https://no-such-host-abc123xyz.invalid/get", timeout=5)
    except Exception as e:
        dt = time.time() - t0
        print(f"  {type(e).__name__} 用时 {dt:.2f}s")
        print(f"  是 ConnectionError 吗 → {isinstance(e, requests.exceptions.ConnectionError)}")
        print(f"  是 Timeout 吗 → {isinstance(e, requests.exceptions.Timeout)}")


def d3_无timeout():
    """D3 不写 timeout 打 /delay/3，记录耗时。"""
    t0 = time.time()
    r = requests.get(BIN + "/delay/3")
    dt = time.time() - t0
    print(f"  无 timeout 打 delay/3: {dt:.2f}s（默认无限等，这次等了 {dt:.1f}s）")
    print(f"  status_code = {r.status_code}")


# ─────────────────────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────────────────────

SECTIONS = {
    "A": [a1_解剖, a2_text与content, a3_乱码修正, a4_json解析失败],
    "B": [b1_404不抛异常, b2_raise_for_status, b3_safe_get],
    "C": [c1_params编码, c2_改UA, c3_None值处理],
    "D": [d1_ReadTimeout, d2_ConnectionError, d3_无timeout],
}


def run(section):
    funcs = SECTIONS[section]
    print("\n" + "=" * 60)
    print(f"{section} 区（{len(funcs)} 题）")
    print("=" * 60)
    for i, fn in enumerate(funcs, 1):
        name = fn.__name__
        print(f"\n[{section}{i}] {name}")
        doc = (fn.__doc__ or "").strip()
        if doc:
            for line in doc.splitlines():
                print("    " + line)
        print("-" * 50)
        try:
            fn()
        except Exception as e:
            print(f"  ❌ 抛异常: {type(e).__name__}: {str(e)[:100]}")


def main():
    arg = sys.argv[1].upper() if len(sys.argv) > 1 else "ALL"

    print("=" * 60)
    print("W2 Day6 · requests GET 练习（13 题）")
    print("=" * 60)
    print(f"  python: {sys.executable}")
    print(f"  requests: {requests.__version__}")
    print(f"  in venv: {sys.prefix != sys.base_prefix}")

    q0_self_test()

    targets = list(SECTIONS) if arg == "ALL" else [arg]
    for sec in targets:
        if sec not in SECTIONS:
            print(f"\n未知分区: {sec}（可选 A/B/C/D/ALL）")
            continue
        run(sec)

    print("\n" + "=" * 60)
    print("全部跑完。把每题的预期填进注释里的 ___，就是今天的结果。")
    print("=" * 60)


if __name__ == "__main__":
    main()
