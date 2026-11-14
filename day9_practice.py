# -*- coding: utf-8 -*-
"""
W2 Day3 · 异常处理练习（数据全部已给好，你只写逻辑）
================================================
用法:  python day9_practice.py
规则:  1) 每题下面有 "# 期望输出:",写完跑一次对答案
       2) B 区必须【先写预测再跑】,预测对错都要记录
       3) 报错一律 as e 打印,禁止手抄报错文本
       4) 禁止裸 except:
讲义:  02-学习内容/12-W2Day3-异常处理.md

分区:
  A 区 6 题  try/except/else/finally 完整形态
  B 区 5 题  预测异常类型(先猜后跑)
  C 区 5 题  raise / 重抛 / 异常链
  D 区 ⭐    自定义 TodoError 家族 + add_todo/get_todo
"""

# ======================================================================
# 0 · 开场自测(不查资料)
# ======================================================================
# 1. try/except/else/finally 四块的执行顺序:
# 答:
# 2. except ValueError as e 里 e 是:
# 答:
# 3. int("abc") / [1][9] / 1/0 各抛什么:
# 答:
# 4. raise 和 return None 报错的区别:
# 答:
# 5. 自定义异常继承谁:
# 答:


# ======================================================================
# A 区 · try 完整形态(6 题)
# ======================================================================
print("\n=== A 区 ===")

# A1 定义 safe_div(a, b):正常返回 a/b;b 为 0 时 except ZeroDivisionError 返回 None
#    测试 safe_div(10, 2) 和 safe_div(10, 0)
# 期望输出: 5.0 None
# 你的函数 ↓
def safe_div(a, b):
    try:
        result = a/b
    except ZeroDivisionError as e:
        return None
    else:
        print("计算成功")
    finally:
        print("运算结束")
    return result

print("A1",safe_div(10, 2),safe_div(10, 0) )


# A2 给 safe_div 加 else 分支:计算成功时打印"计算成功"(必须放 else 里,不放 try 里)
#    再测两条路径,确认 b=0 时不打印"计算成功"
# 期望输出: 计算成功(只在第一条出现)


# A3 给 safe_div 加 finally 分支:打印"运算结束"
#    验证两条路径最后都打印了它
# 期望输出: 两次"运算结束"


# A4 一个 try 配三个 except(ValueError / TypeError / Exception 兜底),
#    用下面三个表达式分别触发,每个 except 里打印分支名 + as e 的信息
# 期望输出: 三个分支各进一次(顺序: ValueError分支 / TypeError分支 / 兜底分支)
expr_a4 = ["int('abc')", "'2' + 2", "1 / 0"]
for expr in expr_a4:
    # 提示: 用 eval(expr) 执行字符串表达式(仅练习用)
    try:
        eval(expr)
    except ValueError as e:
        print(f"{type(e).__name__} : {e}")
    except TypeError as e:
        print(f"{type(e).__name__} : {e}")
    except Exception as e:
        print(f"{type(e).__name__} : {e}")
# A5 触发 int("abc"),用 as e 打印 type(e).__name__ 和 e 本身
# 期望输出: ValueError : invalid literal for int() with base 10: 'abc'
try:
    int('abc')
except ValueError as e:
    print(f"{type(e).__name__} : {e}")

# A6 定义 f_return():try 里 return "try的return",finally 里打印"finally 还是跑了"
#    调用并打印返回值,验证 finally 在 return 之后仍执行
# 期望输出: finally 还是跑了   然后   try的return
# 你的函数 ↓
def f_return():
    try:
        return "try的return"
    except:
        pass
    finally:
        print("finally 还是跑了")

print("A6", f_return())


# ======================================================================
# B 区 · 预测异常类型(先写预测,再跑验证!)
# ======================================================================
print("\n=== B 区 ===")

# B1 表达式: [1, 2, 3][9]
# 我的预测:IndexError
# 实际(跑完填):IndexError : list index out of range
# 你的代码 ↓
try:
    [1, 2, 3][9]
except Exception as e:
    print(f"{type(e).__name__} : {e}")

# B2 表达式: {"a": 1}["b"]
# 我的预测:KeyError
# 实际(跑完填):KeyError
try:
    {"a": 1}["b"]
except Exception as e:
    print(f"{type(e).__name__} : {e}")

# B3 表达式: "2" + 2
# 我的预测:TypeError
# 实际(跑完填):TypeError
try:
    "2" + 2
except Exception as e:
    print(f"{type(e).__name__} : {e}")

# B4 表达式: int("九十二")
# 我的预测:ValueError
# 实际(跑完填):ValueError
try:
    int("九十二")
except Exception as e:
    print(f"{type(e).__name__} : {e}")

# B5 表达式: None.title
# 我的预测:AttributeError
# 实际(跑完填):AttributeError
try:
    None.title
except Exception as e:
    print(f"{type(e).__name__} : {e}")
# B 区统一模板(每题都用这个结构):
# try:
#     表达式
# except Exception as e:
#     print("B1 ->", type(e).__name__, ":", e)


# ======================================================================
# C 区 · raise 与异常链(5 题)
# ======================================================================
print("\n=== C 区 ===")

# C1 定义 withdraw(balance, x):x > balance 时 raise ValueError("余额不足")
#    调用方 try/except 接住,用 as e 打印;再测一次正常的 withdraw(100, 30)
# 期望输出: ValueError : 余额不足   然后   70
# 你的函数 ↓
def withdraw(balance, x):
    if x > balance:
        raise ValueError("余额不足")
    balance-=x
    return balance
try:
    withdraw(100,101)
except ValueError as e:
    print(f"{type(e).__name__} : {e}")



print("C1", withdraw(100, 30))


# C2 内层函数:try 里 1/0,except ZeroDivisionError 里打印"内层记录日志"后【裸 raise】
#    外层再 try/except 接住,打印"外层接到" + type(e).__name__
# 期望输出: 内层记录日志   然后   外层接到 ZeroDivisionError
try:
    try:
      1/0
    except ZeroDivisionError as e:
      print("内层记录日志")
      raise
except Exception as e:
    print(f"外层接到 + {type(e).__name__}")
  
# C3 内层 try 里 int("abc"),except ValueError as e 后
#    raise RuntimeError("包装后的错误") from e
#    外层接住 RuntimeError,打印 e 和 e.__cause__ 的类型
# 期望输出: 包装后的错误   __cause__ 类型: ValueError
try:
    try:
        int("abc")
    except ValueError as e:
        raise RuntimeError("包装后的错误") from e
except RuntimeError as e:
    print(f"{type(e).__name__} : {e} {type(e.__cause__).__name__} : {e.__cause__}")

# C4 定义异常家族:
#    class TodoError(Exception): pass
#    class InvalidIndexError(TodoError): pass
#    class EmptyTitleError(TodoError): pass
# 你的代码 ↓
class TodoError(Exception): pass
class InvalidIndexError(TodoError): pass
class EmptyTitleError(TodoError): pass

# C5 打印两个 issubclass 判断,都应为 True
# 期望输出: True True
print("C5", issubclass(InvalidIndexError,TodoError),issubclass(EmptyTitleError,TodoError))


# ======================================================================
# D 区 · ⭐ 主产出：给 todo 加异常层
# ======================================================================
print("\n=== D 区 ===")

todos_d = ["复习"]

# D1 定义 add_todo(todos, title):
#    title.strip() 为空时 raise EmptyTitleError("标题不能为空")
#    否则 todos.append(title)
# 你的函数 ↓
def add_todo(todos, title):
    if not title.strip():
        raise EmptyTitleError("标题不能为空")
    todos.append(title)


# D2 定义 get_todo(todos, idx):
#    idx < 0 或 idx >= len(todos) 时 raise InvalidIndexError(f"下标 {idx} 越界(共{len(todos)}条)")
#    否则返回 todos[idx]
# 你的函数 ↓
def get_todo(todos, idx):
    if idx < 0 or idx >= len(todos):
        raise InvalidIndexError(f"下标 {idx} 越界(共{len(todos)}条)")
    return todos[idx]


# D3 验收剧本:用 except TodoError as e 接住家族异常
#    依次执行三步:
#      add_todo(todos_d, "  ")     → 应打印 EmptyTitleError : 标题不能为空
#      get_todo(todos_d, 99)       → 应打印 InvalidIndexError : 下标 99 越界(共1条)
#      add_todo(todos_d, "写代码")  → 成功,无异常
#    最后打印 todos_d
#
#    ⚠️ 关键设计:三步要【每步单独包一个 try/except】!
#    如果你把三步放进同一个 try,第一步抛异常后直接跳 except,
#    第二三步根本不会执行 —— 亲手试一次这个坑,再改回来(这是 try 粒度问题)
#
# 期望输出:
#   EmptyTitleError : 标题不能为空
#   InvalidIndexError : 下标 99 越界(共1条)
#   ['复习', '写代码']
try:
    add_todo(todos_d, "  ")
except EmptyTitleError as e:
    print(f"{type(e).__name__} : {e}")

try:
    get_todo(todos_d, 99)
except InvalidIndexError as e:
    print(f"{type(e).__name__} : {e}")

try:
    add_todo(todos_d, "写代码")
except TodoError as e:
    print(f"{type(e).__name__} : {e}")

print(todos_d)
# D4 两个设计问题(答案写进 DAILY.md,不写代码):
#    1) ask_index 用 return None、get_todo 用 raise,同样是编号越界,为什么设计可以不同? 答:因为ask_index 的调用方只有菜单,而且处理方式已知,所以直接return None;而get_todo的处理方式未知,所以用raise
#    2) 如果 todo.py 主循环改用 get_todo + except TodoError,菜单代码会变长还是变短? 答:不确定,菜单代码把if/else换成了try/except,但校验逻辑从主循环挪进了函数
