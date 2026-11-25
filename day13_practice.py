"""day13_practice.py —— W4 Day1：看清 requests 帮你藏起来的报文

对应执行卡: find-job/02-学习内容/W4/24-W4Day1-HTTP请求响应结构.md 练习2
运行: python day13_practice.py
产出: 控制台打印 + http报文解剖.txt（留档，commit 用）
"""

import sys

import requests

# Windows 控制台默认 GBK，中文/符号会炸 UnicodeEncodeError（W1 的老坑）
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

URL = "https://www.baidu.com"
FALLBACK_URL = "https://www.baidu.com"  # wttr.in 不通时的备胎（响应体是HTML，不影响看结构）


def fetch(url: str) -> requests.Response:
    """发 GET，返回响应对象。网络失败时抛 RuntimeError。"""
    try:
        return requests.get(url, timeout=20)
    except requests.exceptions.Timeout:
        raise RuntimeError(f"请求超时（20秒）: {url}")
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"连不上: {url}")


def dissect(r: requests.Response) -> str:
    """把响应报文拆成四部分打印出来，返回全文供存档。"""
    lines = []
    add = lines.append

    add("=" * 60)
    add(f"请求 URL: {r.request.method} {r.url}")
    add("=" * 60)

    # ── ① 状态行 → r.status_code（W2 你判断过 != 200 的那块）──
    add(f"\n【① 状态行】HTTP/1.1 {r.status_code} {r.reason}")

    # ── ② 请求头：requests 实际发出去的（它自动拼的，你以前没看过）──
    add("\n【② 请求头】（requests 自动拼好发出去的）")
    for k, v in r.request.headers.items():
        add(f"  {k}: {v}")

    # ── ③ 空行 + ④ 请求体：GET 通常没有 body ──
    add(f"\n【③④ 空行+请求体】GET 请求 body = {r.request.body!r}（None=没有，验证'GET一般没body'）")

    add("\n" + "-" * 60)

    # ── 响应对称结构：状态行(上面①) / 响应头 / 空行 / 响应体 ──
    add("\n【响应头】")
    for k, v in r.headers.items():
        add(f"  {k}: {v}")

    add("\n【响应体开头 200 字符】")
    add("  " + r.text[:200].replace("\n", "\n  "))

    # ── 三个问题的答案（执行卡练习2要求写在注释里，这里直接给全）──
    ua = r.request.headers.get("User-Agent", "(无)")
    ct = r.headers.get("Content-Type", "(无)")
    add("\n" + "=" * 60)
    add("【练习2 三问三答】")
    add(f"Q1 请求头里有 User-Agent 吗？值是什么？")
    add(f"A1 有。值是 {ua}")
    add(f"   → requests 默认自报家门，网站一眼认出这是脚本不是浏览器。")
    add(f"Q2 响应头的 Content-Type 是什么？和 r.json() 能解析成功有什么关系？")
    add(f"A2 Content-Type = {ct}")
    add(f"   → 它声明'我发的body是什么格式'。application/json 表示body是JSON文本，")
    add(f"     r.json() 才有东西可解析；但 r.json() 成败取决于body实际内容，")
    add(f"     Content-Type 只是服务器的'声明'，声明错了照样解析失败——接口测试要两头都验。")
    add(f"Q3 r.request 是什么对象？")
    add(f"A3 是 PreparedRequest——发出这次请求的那个'请求报文'对象（类型: {type(r.request).__name__}）。")
    add(f"   r 是响应，r.request 是请求，requests 把一问一答绑在一起了。")
    add(f"   所以 r.request.headers 看请求头，r.headers 看响应头，方向别搞反。")

    return "\n".join(lines)


def main():
    try:
        r = fetch(URL)
    except RuntimeError as e:
        print(f"⚠️ {e}，换备胎 {FALLBACK_URL}", file=sys.stderr)
        try:
            r = fetch(FALLBACK_URL)
        except RuntimeError as e2:
            print(f"❌ {e2}\n两个都不通，先看 05-工具手册/03-网络与代理.md 三步排查", file=sys.stderr)
            sys.exit(1)

    report = dissect(r)
    print(report)

    # 留档：跑一次存一份，复盘和 commit 用
    with open("http报文解剖.txt", "w", encoding="utf-8") as f:
        f.write(report + "\n")
    print("\n✅ 已存档到 http报文解剖.txt")


if __name__ == "__main__":
    main()
