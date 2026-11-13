# -*- coding: utf-8 -*-
"""
W1 Day6 · 函数练习（数据全部已给好，你只写函数）
================================================
用法:  python day6_practice.py
规则:  1) 每题下面有 "# 期望输出:",写完跑一次对答案
       2) 不许改上面的数据
       3) 卡住先看讲义: 02-学习内容/08-W1Day6-函数.md

分区:
  A 区 8 题  基础：定义 / 调用 / 返回值 / 默认参数 / 多返回值 / 作用域 / docstring
  B 区 5 题  参数进阶：可变默认参数坑 / *args / **kwargs / 函数作为参数
  C 区 5 题  把 Day5 的代码包成函数
  D 区       ⭐ 今日主产出：重构 todo_v2.py（不在本文件，直接改 todo_v2.py）

⚠️ 不许用 def len / def sum / def max / def print 覆盖内置函数
⚠️ 不许用 global（今天练的是"用 return 交出去"）
"""

# ======================================================================
# 0 · 开场自测(不查资料)
# ======================================================================
# 1. 定义函数的关键字:
# 答:得分
# 2. 不写 return 的函数返回什么:
# 答:空函数
# 3. def f(a, b=1) 里 b 叫什么参数:
# 答:默认参数
# 4. 函数里给变量赋值会改到外面同名变量吗:
# 答:不会
# 5. *args 收进来是什么类型:
# 答:元组


# ======================================================================
# A 区 · 基础(8 题)
# ======================================================================
print("\n=== A 区 ===")

# A1 定义 add(a, b) 返回两数之和;打印 add(2, 3)
# 期望输出: 5
# 你的函数 ↓
def add(a,b):
    return a+b

print("A1", add(2,3))


# A2 定义 is_even(n) 返回是否是偶数;打印 is_even(4) 和 is_even(7)
# 期望输出: True False
# 你的函数 ↓
def is_even(n):
    if n%2==0:
      return True
    else:
      return False

print("A2",is_even(4),is_even(7) )


# A3 定义 greet(name) 返回 f"你好，{name}";打印 greet("张三")
# 期望输出: 你好，张三
# 你的函数 ↓
def greet(name):
    return f"你好,{name}"

print("A3", greet("张三"))


# A4 定义 is_pass(score, line=60) 返回是否 >= line;
#    打印 is_pass(75)、is_pass(75, 80)、is_pass(score=75, line=70)
# 期望输出: True False True
# 你的函数 ↓
def is_pass(score, line=60):
    return True if score>=line else False

print("A4",is_pass(75),is_pass(75, 80),is_pass(score=75, line=70) )


# A5 定义 min_max(nums) 一次返回最小值和最大值;
#    先打印整个返回值,再解包成 lo, hi 打印
# 期望输出: (1, 5)   然后   1 5
# 你的函数 ↓
def min_max(nums):
    nums=sorted(nums)
    return nums[0],nums[len(nums)-1]
a,b=min_max([5,4,3,2,1])
print("A5",min_max([5,4,3,2,1]),a,b )


# A6 定义 no_return(x),函数体只写 x * 2,故意不 return;打印调用结果
# 期望输出: None
# 你的函数 ↓
def no_return(x):
   x*2

print("A6",no_return(1) )


# A7 外部已有 x = 100。定义 show_scope() 在内部 x = 200 并打印;
#    调用它,然后再打印外部的 x
# 期望输出: 函数内 200   函数外 100
x = 100
# 你的函数 ↓
def show_scope():
    x=200
    print(x)
show_scope()

print("A7",x )


# A8 定义 area(w, h),第一行写 docstring(说明干什么/参数/返回),返回面积;
#    打印 area.__doc__ 的第一行
# 期望输出: 计算矩形面积。
# 你的函数 ↓
def area(w, h):
    """计算矩形面积

    参数:w 宽,h 高
    返回:矩形面积(数字)
    """
    return w*h

print("A8", area.__doc__)


# ======================================================================
# B 区 · 参数进阶(5 题)
# ======================================================================
print("\n=== B 区 ===")

# B1 复现坑:定义 bad_append(x, lst=[]),append 后 return lst;连调两次并打印
# 期望输出: [1] 然后 [1, 2]   ← 第二次带着上一次的数据
# 你的函数 ↓
def bad_append(x, lst=[]):
    lst.append(x)
    return lst


print("B1",bad_append(1))
print(bad_append(2))


# B2 修好它:定义 good_append(x, lst=None),lst 为 None 时新建列表;连调两次
# 期望输出: [1] 然后 [2]
# 你的函数 ↓
def good_append(x, lst=None):
    if lst == None:
        lst=[]
    lst.append(x)
    return lst

print("B2", good_append(1))
print(good_append(2))


# B3 定义 total(*nums) 返回所有数的和;打印 total(1, 2, 3, 4)
# 期望输出: 10
# 你的函数 ↓
def total(*nums):
    ans=0
    for n in nums:
        ans+=n
    return ans

print("B3", total(1, 2, 3, 4))


# B4 定义 show(**kwargs) 返回 kwargs;打印 show(name="张三", score=85)
# 期望输出: {'name': '张三', 'score': 85}
# 你的函数 ↓
def show(**kwargs):
    return kwargs

print("B4", show(name="张三", score=85))


# B5 定义 get_score(s) 返回 s["score"];
#    用它排序 people,打印排好序的人名列表
#    ★ 这题会让你明白 sorted(key=...) 里的 key 要的到底是什么
# 期望输出: ['李四', '张三', '王五']
people_b = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
]
# 你的函数 ↓
def get_score(s):
    return s["score"]
print("B5", [p["name"] for p in sorted(people_b,key=get_score,reverse=True)])


# ======================================================================
# C 区 · 把 Day5 的代码包成函数(5 题)
# ======================================================================
print("\n=== C 区 ===")

# C1 定义 count_words(text) 返回每个单词出现次数;打印 count_words(text)
# 期望输出: {'a': 3, 'b': 2, 'c': 1}
# 提示: split() 按单词切,别忘了给参数就是按空白切
text_c = "a b a c b a"
# 你的函数 ↓
def count_words(text):
    ans={}
    for t in text.split():
        ans[t]=ans.get(t,0)+1
    return ans


print("C1", count_words(text_c))


# C2 定义 find_best(d) 返回分数最高的人名;打印 find_best(students_c)
# 期望输出: 李四
students_c = {"张三": 85, "李四": 92, "王五": 78}
# 你的函数 ↓
def find_best(d):
    max=0
    ans=""
    for k,v in d.items():
        if v > max:
            max=v
            ans=k
        
    return ans
print("C2", find_best(students_c))


# C3 定义 format_params(d) 返回 "name=张三&score=85" 这种一行;打印它
# 期望输出: name=张三&score=85
pairs_c = {"name": "张三", "score": 85}
# 你的函数 ↓
def format_params(d):
    return "&".join(f"{k}={v}" for k, v in d.items())

print("C3", format_params(pairs_c))


# C4 定义 top_n(people, n) 返回分数最高的前 n 个名字(按分数从高到低);
#    打印 top_n(people_c, 2) 和 top_n(people_c, 3)
# 期望输出: ['李四', '张三']   然后   ['李四', '张三', '王五']
people_c = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
]
# 你的函数 ↓
def top_n(people, n):
    ans=[p["name"] for p in sorted(people,key=get_score,reverse=True)]
    return ans[:n]

print("C4", top_n(people_c, 2),top_n(people_c, 3))



# C5 定义 group_by(people, line=80) 返回 {"及格": [名字...], "不及格": [名字...]};
#    打印 group_by(people_c) 和 group_by(people_c, 90)
# 期望输出: {'及格': ['张三', '李四'], '不及格': ['王五']}
#           然后 {'及格': ['李四'], '不及格': ['张三', '王五']}
# 你的函数 ↓
def group_by(people, line=80):
    ans={"及格":[],"不及格":[]}
    for k in people:
        if k["score"] > line:
            ans["及格"].append(k["name"])
        else:
            ans["不及格"].append(k["name"])
    return ans
print("C5", group_by(people_c),group_by(people_c, 90))


# ======================================================================
# D 区 · ⭐ 今日主产出：重构 todo_v2.py（不在本文件写）
# ======================================================================
# 目标: 把 "标记完成" 和 "删除" 两段里重复的 8 行抽成 ask_index()
#
# def ask_index(prompt, todos):
#     """提示输入编号，校验后返回 0 基下标；输入非法返回 None。
#
#     参数: prompt 提示语, todos 当前列表（用来判断越界）
#     返回: int 下标 或 None
#     """
#     # 你的代码
#
# 四条要求:
#   1) 输入 abc  -> 打印"输入无效，请输入数字", 返回 None
#   2) 输入 0/99 -> 打印"输入编号无效!",       返回 None
#   3) 输入 2    -> 返回 1   （1基转0基在函数里做掉）
#   4) 不打印"已标记完成"、不调 save_todos —— 只管拿到合法下标
#
# 验收: 改完跑 todo_v2.py，把这 5 个输入各试一遍，都不能崩：
#   加一条 → 列出 → 标记(abc) → 标记(0) → 标记(99) → 标记(1) → 删除(1) → q → 重开 → 还在
#
# 判据: grep "请输入你已完成" todo_v2.py 只剩 1 处（提示语不再重复）
