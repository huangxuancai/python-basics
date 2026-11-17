"""weather_cli.py —— 命令行天气查询工具

用法:
    python weather_cli.py <城市名>
    python weather_cli.py Beijing
    python weather_cli.py Shanghai

数据来源: wttr.in（公开免费，无需 API key）
提示: 推荐使用英文或拼音城市名，中文识别可能不准
"""

import sys

import requests


def get_weather(city: str) -> str:
    """查询城市天气，返回格式化字符串。

    Args:
        city: 城市名（推荐英文/拼音，如 Beijing、Shanghai）

    Returns:
        格式化的天气信息字符串

    Raises:
        RuntimeError: 网络失败或城市不存在时
    """
    url = f"https://wttr.in/{city}?format=j1"

    # ── 请求阶段 ──
    try:
        r = requests.get(url, timeout=20)
    except requests.exceptions.Timeout:
        raise RuntimeError("请求超时（20 秒），wttr.in 可能繁忙，请稍后重试")
    except requests.exceptions.ConnectionError:
        raise RuntimeError("连不上 wttr.in，检查网络连接")

    # ── 状态码检查（wttr.in 对不存在的城市返回 500 + 纯文本）──
    if r.status_code != 200:
        msg = r.text.strip()[:100] if r.text else f"HTTP {r.status_code}"
        raise RuntimeError(f"查询失败: {msg}")

    # ── JSON 解析 ──
    try:
        d = r.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("返回数据格式异常，无法解析")

    # ── 提取当前天气 ──
    cw = d["current_condition"][0]
    area = d["nearest_area"][0]["areaName"][0]["value"]
    temp = cw["temp_C"]
    feels = cw["FeelsLikeC"]
    humidity = cw["humidity"]
    desc = cw["weatherDesc"][0]["value"]
    wind = cw["windspeedKmph"]
    winddir = cw["winddir16Point"]

    # ── 格式化输出 ──
    lines = [
        f"📍 {area} 当前天气",
        f"   🌡️  {temp}°C（体感 {feels}°C）",
        f"   💧 湿度 {humidity}%  💨 {winddir} {wind}km/h",
        f"   ☁️  {desc}",
        "",
        "📅 未来 3 天预报",
    ]

    for w in d["weather"]:
        date = w["date"]
        hi = w["maxtempC"]
        lo = w["mintempC"]
        lines.append(f"   {date}  {lo}°C ~ {hi}°C")

    return "\n".join(lines)


def main():
    """命令行入口。"""
    if len(sys.argv) < 2:
        print("用法: python weather_cli.py <城市名>")
        print("示例: python weather_cli.py Beijing")
        print("      python weather_cli.py Shanghai")
        print("提示: 推荐使用英文或拼音城市名")
        sys.exit(1)

    city = sys.argv[1]

    try:
        result = get_weather(city)
        print(result)
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
