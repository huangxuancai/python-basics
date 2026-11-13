# -*- coding: utf-8 -*-
"""
W2 Day1 · 函数进阶练习（数据全部已给好，你只写逻辑）
================================================
用法:  python day7_practice.py
规则:  1) 每题下面有 "# 期望输出:",写完跑一次对答案
       2) 不许改上面的数据
       3) 卡住先看讲义: 02-学习内容/10-W2Day1-函数进阶.md

分区:
  A 区 6 题  列表推导式基础
  B 区 5 题  字典推导 + 生成器 + 解包
  C 区 5 题  综合实战（把 W1 的代码用推导式重写）
  D 区       ⭐ 重构 day6_practice.py C 区（不在本文件写）

⚠️ 变量名不许叫 list / dict / sum / max / min
"""

# ======================================================================
# 0 · 开场自测(不查资料)
# ======================================================================
# 1. [x*x for x in range(4)] =
# 答:[0,1,4,9]
# 2. [x for x in range(6) if x % 2 == 0] =
# 答:[0,2,4]
# 3. lambda x: x+1 和 def f(x): return x+1 的区别:
# 答:没区别
# 4. (x*x for x in range(5)) 的类型是:
# 答:元组
# 5. show(*(1,2,3)) 里 * 的作用是:
# 答: 解包



# ======================================================================
# A 区 · 列表推导式基础(6 题)
# ======================================================================
print("\n=== A 区 ===")

nums_a = [85, 42, 92, 55, 78, 60]
words_a = ["hello", "world", "python"]

# A1 用推导式生成 0-5 的平方列表
# 期望输出: [0, 1, 4, 9, 16, 25]
print("A1",[x*x for x in range(6)] )


# A2 从 nums_a 中筛选 >= 60 的成绩
# 期望输出: [85, 92, 78, 60]
print("A2",[n for n in nums_a if n >= 60] )


# A3 把 words_a 全部转大写
# 期望输出: ['HELLO', 'WORLD', 'PYTHON']
print("A3", [word.upper() for word in words_a])


# A4 从 nums_a 生成 (数, 平方) 配对列表
# 期望输出: [(85, 7225), (42, 1764), (92, 8464), (55, 3025), (78, 6084), (60, 3600)]
print("A4", [(x,x*x) for x in nums_a])


# A5 用三元表达式:偶数标"偶",奇数标"奇"(range(6))
# 期望输出: ['偶', '奇', '偶', '奇', '偶', '奇']
print("A5", ["偶" if x % 2 == 0 else "奇" for x in range(6)])


# A6 把 A2 的传统 for+append 写法也写一遍,验证结果相同
# 期望输出: True
traditional = []
# 你的传统写法 ↓
for i in nums_a:
    if i >= 60:
        traditional.append(i)

print("A6", traditional == [85, 92, 78, 60])


# ======================================================================
# B 区 · 字典推导 + 生成器 + 解包(5 题)
# ======================================================================
print("\n=== B 区 ===")

rev_b = {"a": 1, "b": 2, "c": 3}


def add3(a, b, c):
    return a + b + c

args_b = (1, 2, 3)
kwargs_b = {"a": 10, "b": 20, "c": 30}

# B1 {x: x*x for x in range(5)}
# 期望输出: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
print("B1", {x: x*x for x in range(5)})


# B2 反转 rev_b(value → key)
# 期望输出: {1: 'a', 2: 'b', 3: 'c'}
print("B2",{v:k for k,v in rev_b.items()} )


# B3 从 students_b 生成 {名字: 分数}
# 期望输出: {'张三': 85, '李四': 92, '王五': 78}
students_b = [("张三", 85), ("李四", 92), ("王五", 78)]
print("B3", {stu[0]:stu[1] for stu in students_b})


# B4 生成器表达式 (x*x for x in range(5)),打印类型和 sum
# 期望输出: generator 然后 30
g = (x*x for x in range(5))  # ← 改成真正的生成器表达式
print("B4", type(g).__name__)
print("B4 sum", sum(g))


# B5 用 * 解包 args_b 调用 add3;用 ** 解包 kwargs_b 调用 add3
# 期望输出: 6 然后 60
print("B5",add3(*args_b) )
print("B5",add3(**kwargs_b) )


# ======================================================================
# C 区 · 综合实战(5 题)
# ======================================================================
print("\n=== C 区 ===")

text_c = "a b a c b a"
people_c = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
]
pairs_c = {"name": "张三", "score": 85}
matrix_c = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# C1 用推导式统计 text_c 词频(提示:set(text_c.split())去重,.count()计数)
# 期望输出: {'a': 3, 'b': 2, 'c': 1}
ans={}
for t in text_c.split():
    ans[t]=ans.get(t,0)+1
print("C1", ans)


# C2 用推导式从 people_c 取分数 >= 80 的名字列表
# 期望输出: ['张三', '李四']
print("C2", [p["name"] for p in people_c if p["score"] >= 80])


# C3 用推导式把 pairs_c 拼成 "name=张三&score=85"
# 期望输出: name=张三&score=85
print("C3","&".join(f"{k}={v}" for k,v in pairs_c.items()))


# C4 用推导式把 matrix_c 展平成一维列表
# 期望输出: [1, 2, 3, 4, 5, 6, 7, 8, 9]
print("C4", [x for m in matrix_c for x in m])


# C5 用推导式生成 [{"title": "任务1", "done": False}, ...] (i=1,2,3)
# 期望输出: [{'title': '任务1', 'done': False}, {'title': '任务2', 'done': False}, {'title': '任务3', 'done': False}]
print("C5", [{"title": f"任务{i}", "done": False} for i in range(1, 4)])


# ======================================================================
# D 区 · ⭐ 重构 day6_practice.py C 区（不在本文件写）
# ======================================================================
# 打开 day6_practice.py,C 区 5 个函数里找至少 2 处能用推导式简化的地方
# 改完跑 python day6_practice.py 确认输出不变
#
# 提示:
#   - count_words: 计数模式用推导式反而不清晰,可以不改
#   - format_params: "&".join(f"{k}={v}" for k,v in d.items()) 已经在用了
#   - top_n: [p["name"] for p in sorted(...)[:n]] 已经在用了
#   - group_by: 试试能不能用推导式(提示:不太适合,因为要往两个列表分别 append)
#   - find_best: max(d, key=d.get) 已经是最简了
#
# 如果找不到可简化的,就把 C1-C5 里任意两题的传统写法补在注释里作对比
