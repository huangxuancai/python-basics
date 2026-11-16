# -*- coding: utf-8 -*-
"""
W2 Day4 · 模块与包练习
================================================
用法:  python day10_practice.py
规则:  1) 每题下面有 "# 期望输出:",写完跑一次对答案
       2) B 区要先新建 mytool.py,C 区要先新建 myutils.py(要求写在题里)
       3) 报错一律 as e 打印,禁止手抄报错文本
讲义:  02-学习内容/13-W2Day4-模块与包.md

分区:
  A 区 6 题  import 四形态 + sys.path + 缓存
  B 区 4 题  __name__ 两态实验(新建 mytool.py)
  C 区 4 题  自建工具模块(新建 myutils.py,搬旧函数)
  D 区 3 题  json 对比手写 CSV + pip 命令
  主产出     todo.py 拆三件套(不在本文件,见讲义第 5 节)
"""

# ======================================================================
# 0 · 开场自测(不查资料)
# ======================================================================
# 1. import math 和 from math import sqrt 用起来的区别:
# 答:
# 2. Python 去哪里找你 import 的模块:
# 答:
# 3. __name__ == "__main__" 什么时候为真:
# 答:
# 4. 一个目录要成为"包",里面要有什么文件:
# 答:
# 5. 装第三方包的命令:
# 答:


# ======================================================================
# A 区 · import 基础(6 题)
# ======================================================================
print("\n=== A 区 ===")

# A1 import math,打印 math.sqrt(144) 和 math.pi(保留2位)
# 期望输出: 12.0 3.14
print("A1", )


# A2 from random import randint,生成一个 1-10 的数打印(每次不同是对的)
# 期望输出: 1-10 之间的一个整数
print("A2", )


# A3 import datetime as dt,打印 dt.date.today()
# 期望输出: 2026-11-16(当天日期)
print("A3", )


# A4 打印 sys.path[0],确认是你的项目目录
# 期望输出: C:\Users\-\Desktop\study_Python-Basics_20251108_v1.0\python-basics
print("A4", )


# A5 用 dir(math) 看 math 里有哪些名字,打印前 8 个
# 期望输出: ['__doc__', '__loader__', '__name__', ...] 这样的列表
print("A5", )


# A6 同一个模块 import 两次,两次之间 print 一句话
#    验证:模块顶层只执行一次(第二次 import 无任何输出)
#    提示: import math 两次即可(math 顶层没打印,所以配合 B 区的 mytool 更直观;
#          这里先用 id(math) is id(math) 或打印两次 import 之间的那句话验证不报错)
# 期望输出: 两次 import 之间的那句话只出现一次上下文
print("A6", )


# ======================================================================
# B 区 · __name__ 两态实验(4 题)
# ======================================================================
# 先新建 mytool.py(和 day10_practice.py 同目录),内容要求:
#   1. 顶层一句: print(f"[mytool] 顶层执行, __name__={__name__}")
#   2. 函数 double(x): 返回 x*2
#   3. if __name__ == "__main__": 守卫里 print("直接运行自检:", double(21))
print("\n=== B 区 ===")

# B1 在 PowerShell 里: python mytool.py
#    期望: 顶层行(__name__=__main__) + 自检行 double(21)=42 都出现
#    看到的输出抄这里:


# B2 建好 mytool.py 后,取消下面这行的注释,再跑本文件
#    期望: 只出现顶层行(__name__=mytool),自检行不出现
# import mytool   # ← mytool.py 建好后取消注释（不建就取消注释的话,整个文件 ModuleNotFoundError）


# B3 调用 mytool.double(5)
# 期望输出: 10
print("B3", )


# B4 再写一遍 import mytool(第二遍)
#    期望: [mytool] 顶层行只打印过一次(缓存生效)
# import mytool   # ← 第二遍,同样建好文件后取消注释
print("B4 第二次 import 完成,上面没有再出现顶层行 = 缓存生效")


# ======================================================================
# C 区 · 自建工具模块 myutils.py(4 题)
# ======================================================================
# 先新建 myutils.py,要求:
#   1. count_words(text)  ← 从 day6_practice.py C1 搬过来(词频统计)
#   2. format_params(d)   ← 从 day6_practice.py C3 搬过来("&".join 版)
#   3. 文件末尾 if __name__ == "__main__": 自检,两个函数各调用打印一次
print("\n=== C 区 ===")

text_c = "a b a c b a"
pairs_c = {"name": "张三", "score": 85}

# C1 在 PowerShell 里: python myutils.py → 自检输出正常
#    看到的输出抄这里:


# C2 from myutils import count_words, format_params,调用并打印
# 期望输出: {'a': 3, 'b': 2, 'c': 1} 和 name=张三&score=85
# 你的代码 ↓


print("C2", )


# C3 换成 import myutils as mu 的方式再调一遍(mu.count_words / mu.format_params)
# 期望输出: 和 C2 相同
# 你的代码 ↓


print("C3", )


# C4 故意 import 一个不存在的模块,用 try/except 接住并 as e 打印
# 期望输出: ModuleNotFoundError : No module named '不存在的模块xyz'
# 你的代码 ↓



# ======================================================================
# D 区 · json 对比 + pip(3 题)
# ======================================================================
print("\n=== D 区 ===")

todos_d = [{"title": "买牛奶,面包", "done": False}]

# D1 手写 CSV 格式序列化再读回,见证数据损坏:
#    line = f"{todos_d[0]['title']},{1 if todos_d[0]['done'] else 0}"
#    row = line.strip().split(",")
#    打印 line 和 row
# 期望输出: '买牛奶,面包,0' 然后 ['买牛奶', '面包', '0']  ← 标题被切成两半!
print("D1", )


# D2 用 json 做同一件事:
#    import json
#    s = json.dumps(todos_d, ensure_ascii=False)
#    back = json.loads(s)
#    打印 s、back、back == todos_d
# 期望输出: [{"title": "买牛奶,面包", "done": false}] / [{'title': '买牛奶,面包', 'done': False}] / True
print("D2", )


# D3 在 PowerShell 里跑(不是写代码):
#    python -m pip list | Select-String requests
#    python -m pip show requests
#    把 requests 的版本号抄这里:
# 答:


# ======================================================================
# 主产出 · todo.py 拆三件套(见讲义第 5 节,不在本文件写)
# ======================================================================
# 目标结构:
#   todo_errors.py  ← TodoError / InvalidIndexError / EmptyTitleError
#   todo_core.py    ← Todo 类 + TODO_FILE + load/save/add/get + __main__ 自检
#   todo.py         ← 菜单界面层 + main() + if __name__ == "__main__": main()
#
# 拆分四步(每步跑一次):
#   1. 建 todo_errors.py,搬三个异常类
#   2. 建 todo_core.py,搬 Todo 类 + 存取函数,顶部 from todo_errors import ...
#   3. todo.py 瘦身:只留界面,from todo_core import ...,主循环包进 main()
#   4. "添加"分支改用 add_todo + except TodoError(接上 Day3 的成果)
#
# 验收四条:
#   python todo_core.py           → 自检打印读到 N 条
#   python -c "import todo_core"  → 没有自检输出(守卫生效)
#   python todo.py                → 全功能回归,输出与拆分前一字不差
#   添加时直接回车                 → EmptyTitleError: 标题不能为空
#
# 依赖方向必须单向: todo.py → todo_core.py → todo_errors.py
# 反向 import(如 todo_core import todo)= 循环导入,当场报错(错误实验②)
