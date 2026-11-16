# -*- coding: utf-8 -*-
"""
W2 Day5 · 虚拟环境与 requirements 练习
================================================
用法:  venv\\Scripts\\python.exe day11_practice.py     ← 用 venv 的解释器跑
       （激活后也可以: python day11_practice.py）
规则:  1) 每题下面有 "# 期望:",写完跑一次对答案
       2) 标了 [shell] 的题是命令行题，把实测输出抄进答案的字符串里
       3) 报错一律 as e 打印，禁止手抄报错文本
讲义:  02-学习内容/14-W2Day5-虚拟环境与requirements.md

分区:
  A 区 6 题  建环境与观察（pyvenv.cfg / sys.prefix / 文件数与体积）
  B 区 4 题  隔离验证（venv 有、全局没有）
  C 区 4 题  requirements.txt（读、解析、编码、版本约束）
  D 区 3 题  git 与 .gitignore
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VENV = HERE / "venv"


# ======================================================================
# 0 · 开场自测（先别看讲义，写完再对）
# ======================================================================
# 1. 虚拟环境解决的核心问题是什么？
# 答:
# 2. `python -m venv venv` 里第二个 venv 指的是什么？
# 答:
# 3. 激活虚拟环境，改的是什么？
# 答:
# 4. 判断"我在不在虚拟环境里"最可靠的一行代码：
# 答:
# 5. venv 目录为什么不进 git？那别人怎么拿到一样的包？
# 答:


# ======================================================================
# A 区 · 建环境与观察（6 题）
# ======================================================================
print("\n=== A 区 ===")

# A1 [shell] 建环境花了多久？把实测秒数写进来
# 期望: 5-10 秒（本机 6.2 秒）
a1_耗时 = "___"  # ← 填数字，例如 "6.2 秒"
print("A1  建环境耗时:", a1_耗时)


# A2 打印 venv 的文件数和体积（自己遍历，别调 shell）
# 期望: 约 2299 个文件 / 32 MB（刚建好时 1497 个 / 26 MB）
def a2_统计(root: Path):
    if not root.exists():
        return None
    files = [p for p in root.rglob("*") if p.is_file()]
    total = sum(p.stat().st_size for p in files)
    return len(files), total


stat = a2_统计(VENV)
if stat:
    n, size = stat
    print(f"A2  venv: {n} 个文件，{size / 1024 / 1024:.1f} MB")
else:
    print("A2  venv 不存在，先跑 python -m venv venv")


# A3 读 pyvenv.cfg 的 home 和 include-system-site-packages
# 期望: home 指向 D:\\env_Python311_20261105_v1.0 ；include-system-site-packages = false
cfg = VENV / "pyvenv.cfg"
if cfg.exists():
    conf = {}
    for line in cfg.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            conf[k.strip()] = v.strip()
    print("A3  home =", conf.get("home"))
    print("A3  include-system-site-packages =", conf.get("include-system-site-packages"))
    print("A3  version =", conf.get("version"))
else:
    print("A3  pyvenv.cfg 不存在")


# A4 [shell] 不激活，直接跑 venv 的 exe 看版本
# 命令: venv\\Scripts\\python.exe -V
# 期望: Python 3.11.9（不激活也能跑，venv 的 exe 自带定位能力）
a4_输出 = "___"
print("A4  不激活直接跑:", a4_输出)


# A5 打印 sys.prefix 和 sys.base_prefix，判断自己在不在 venv 里
# 期望: 两个值不同 → 在 venv 里；相同 → 在全局
print("A5  sys.prefix      =", sys.prefix)
print("A5  sys.base_prefix =", sys.base_prefix)
print("A5  在 venv 里吗:", sys.prefix != sys.base_prefix)


# A6 数 venv 里 site-packages 有多少个包
# 期望: 8 个（pip / setuptools / requests 及其 4 个依赖 / pyfiglet）
site_packages = VENV / "Lib" / "site-packages"
if site_packages.exists():
    pkgs = sorted(
        d.name
        for d in site_packages.iterdir()
        if d.is_dir() and not d.name.startswith("_") and not d.name.endswith(".dist-info")
    )
    print(f"A6  site-packages: {len(pkgs)} 个目录 →", ", ".join(pkgs))
    print("     （其中 pkg_resources 是 setuptools 附带的，真正的包 8 个）")
else:
    print("A6  site-packages 不存在")


# ======================================================================
# B 区 · 隔离验证（4 题）
# ======================================================================
print("\n=== B 区 ===")

# B1 看当前解释器能不能 import requests，并打印版本
# 期望: 在 venv 里 → 2.34.2；在全局 → 也是 2.34.2（但这是两个不同的副本）
try:
    import requests

    print("B1  requests", requests.__version__)
    print("     位置:", Path(requests.__file__).parent)
except ModuleNotFoundError as e:
    print("B1  没装:", e)


# B2 用一个"全局有、venv 没有"的包验证隔离
# 提示: 全局有 471 个包，随便挑一个 venv 里没有的（如 numpy）
# 期望: ModuleNotFoundError: No module named 'numpy'
try:
    import numpy

    print("B2  numpy 竟然能导入，版本", numpy.__version__, "→ 这个环境不干净")
except ModuleNotFoundError as e:
    print("B2  隔离成功:", type(e).__name__, "-", e)


# B3 当前环境里 pip 的版本（venv 是 24.0，全局是 26.3）
# 期望: 24.0（说明你跑的是 venv 自带的老 pip）
from importlib.metadata import version

print("B3  pip =", version("pip"), "| setuptools =", version("setuptools"))


# B4 [shell] 对比 venv 和全局的 freeze 行数
# 命令: venv\\Scripts\\python.exe -m pip freeze | Measure-Object -Line
#       python -m pip freeze | Measure-Object -Line      （全局）
# 期望: 6 行 vs 471 行
b4_venv行数 = "___"
b4_全局行数 = "___"
print(f"B4  venv {b4_venv行数} 行 vs 全局 {b4_全局行数} 行")


# ======================================================================
# C 区 · requirements.txt（4 题）
# ======================================================================
print("\n=== C 区 ===")

REQ = HERE / "requirements.txt"


def detect_encoding(p: Path) -> str:
    """靠 BOM 判断编码。没 BOM 就当 utf-8（本文件遇到的两种真实情况都覆盖了）。"""
    head = p.read_bytes()[:4]
    if head.startswith(b"\xff\xfe") or head.startswith(b"\xfe\xff"):
        return "utf-16"  # PowerShell 的 > 干的
    if head.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    return "utf-8"


enc = "utf-8"
if REQ.exists():
    enc = detect_encoding(REQ)

# C2 先做：检查文件编码，决定后面怎么读
# 期望: 没有 BOM（= 用的是 Set-Content -Encoding ascii 或 cmd 重定向）
#      如果是 UTF-16 → 你在 PowerShell 里用了 > ，重做第 6.3 节
if REQ.exists():
    head = REQ.read_bytes()[:2]
    if head == b"\xff\xfe":
        print("C2  ⚠️ 是 UTF-16LE（PowerShell > 的产物）→ 重新生成：")
        print('      python -m pip freeze | Set-Content requirements.txt -Encoding ascii')
    elif head == b"\xef\xbb\xbf":
        print("C2  是 UTF-8 带 BOM（能读，但建议去掉）")
    else:
        print("C2  ✅ 干净编码，前两字节 =", head, "| 按", enc, "读")

# C1 逐行读 requirements.txt，打印每一行（跳过空行和注释）
# 期望: certifi==... / charset-normalizer==... / idna==... / pyfiglet==... / requests==... / urllib3==...
# 注意：PowerShell 的 > 会写成 UTF-16，硬编码 utf-8 读会 UnicodeDecodeError。所以先探测再读。
lines = []
if REQ.exists():
    lines = [
        ln.strip() for ln in REQ.read_text(encoding=enc).splitlines() if ln.strip() and not ln.startswith("#")
    ]
    print(f"C1  requirements.txt 有效行 {len(lines)} 条（按 {enc} 解码）:")
    for ln in lines:
        print("     ", ln)
else:
    print("C1  requirements.txt 不存在，先跑 pip freeze 生成")


# C3 解析版本约束：把 == 和 >= 区分开
# 期望: 精确锁 5 条 / 范围 1 条（看你怎么写的）
if REQ.exists():
    pin = [ln for ln in lines if "==" in ln]
    rng = [ln for ln in lines if ">=" in ln or "<" in ln]
    print(f"C3  精确锁定 {len(pin)} 条，范围约束 {len(rng)} 条")
    print("     精确:", ", ".join(pin))
    if rng:
        print("     范围:", ", ".join(rng))


# C4 一个"包里没有这个名字"的报错长什么样
# 期望: ModuleNotFoundError: No module named 'reqests'   ← 少一个 u
try:
    import reqests  # noqa: F401  故意写错
except ModuleNotFoundError as e:
    print("C4  ", type(e).__name__, "-", e)


# ======================================================================
# D 区 · git 与 .gitignore（3 题）
# ======================================================================
print("\n=== D 区 ===")


def git(*args: str) -> str:
    """跑一条 git 命令，返回 stdout；git 不可用时返回错误说明。"""
    import subprocess

    try:
        r = subprocess.run(
            ["git", *args], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        return (r.stdout or r.stderr).strip()
    except FileNotFoundError:
        return "（没装 git）"


# D1 看 venv 有没有被 git 忽略
# 期望: 输出 "venv/" → 说明 .gitignore 里有这条规则
d1 = git("check-ignore", "venv/")
print("D1  check-ignore venv/ →", d1 or "（没有被忽略！去改 .gitignore）")


# D2 数一下现在有多少未跟踪文件
# 期望: 加了 venv/ 之后只剩 1-2 个（requirements.txt / day11_practice.py）
d2 = git("status", "--short", "--untracked-files=all")
count = len([ln for ln in d2.splitlines() if ln.strip()])
print(f"D2  未跟踪/已修改 {count} 个:")
for ln in d2.splitlines()[:8]:
    print("     ", ln)
if count > 8:
    print("      ...")


# D3 打印当前分支和最后一次提交
# 期望: master / main + Day4 那条 commit
print("D3  分支:", git("rev-parse", "--abbrev-ref", "HEAD"))
print("D3  最后提交:", git("log", "--oneline", "-1"))


# ======================================================================
# 收尾 · 用一条命令确认"我现在到底在哪"
# ======================================================================
print("\n=== 总结 ===")
in_venv = sys.prefix != sys.base_prefix
print("解释器:", sys.executable)
print("在 venv 里:", in_venv)
if in_venv:
    print("✅ 你现在跑的是 venv 里的 Python，装包不会污染全局")
else:
    print("⚠️ 你在全局 Python 里跑，装包会进那 471 个包的环境")
print("\n跑完记得把 A1-A4、B4 那几个 [shell] 题的实测值填回去。")
