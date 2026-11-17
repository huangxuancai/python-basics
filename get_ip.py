"""get_ip.py —— 查本机公网 IP"""
import sys
import requests

def main():
    try:
        r = requests.get("https://httpbin.org/ip",timeout=10)
        r.raise_for_status()
        ip=r.json()["origin"]
        print(f"本机公网 IP:{ip}")
    except requests.exceptions.Timeout:
        print("请求超时，检查网络或加大 timeout", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("连不上 httpbin.org，检查网络/域名/代理", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"服务器返回 {e.response.status_code} {e.response.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()