# -*- coding: utf-8 -*-
"""
W1 Day5 · 字符串方法与文件读写 练习骨架
================================================
用法:  python day5_practice.py
规则:  1) 每写完 3-5 行就运行一次, 不要一次写完再跑
       2) 报错只读最后一行, 抄进注释, 写一句中文原因
       3) 禁止截图, 笔记就是这里的注释
       4) ★ A / B / C 三区的数据都已经给好了, 不要改、不要重抄, 你只写逻辑
讲义:  C:\\Users\\-\\Desktop\\project_Job-Hunt_20251108_v1.0\\02-学习内容\\06-W1Day5-字符串与文件.md

分区:
  A 区  字符串 8 个方法 + 8 道题      (09:00-10:30)
  B 区  文件读写 6 个实验              (上午)
  E 区  故意写错的 5 条, 报错抄这里    (下午任意时间)
  C 区  实战 T1-T7                     (14:00-16:30)

⚠️ 今天的两个主产出不在这个文件里:
   todo_v2.py  ← 给 Day4 的 todos 加持久化(新建文件)
   todo.txt    ← 程序生成的, 不要手写

⚠️ 只要文件里有中文, 读写两端都写 encoding="utf-8"
   本机默认编码是 cp936(GBK), 混用会 UnicodeDecodeError
"""

# ======================================================================
# 0 · 开场自测(不查资料, 先把答案写在下面, 写完再往下看讲义)
# ======================================================================
# 1. "  a b  ".strip() =
# 答:"ab"
# 2. "a,b,c".split(",") =
# 答:"a","b","c"
# 3. ["a","b","c"] 变成 "a-b-c" 怎么写:
# 答:不知道
# 4. 打开文件写入, open 的第二个参数写什么字母:
# 答:不知道
# 5. 文件用完了要做什么:
# 答:关掉


# ======================================================================
# A 区 · 字符串(09:00-10:30)  —— 数据已给好
# ======================================================================
s = "  Hello World  \n"          # A1 / 8 个方法用
fruit_text = "apple,banana,cherry" # A2
names_for_join = ["张三", "李四", "王五"]   # A3
numbers_for_join = [85, 92, 78]   # A4
dash_text = "a-b-c-d"             # A5
hello = "Hello"                   # A6
filename = "test_login.py"        # A7


# --- 8 个方法: 每个敲一遍, 敲完注释一句"这行在干嘛"
# print(repr(s))            # repr 能把空格和换行显形, print(s) 看不出来
print(repr(s))  
# print(repr(s.strip()))    # 这行在干嘛: 去两端空白
print(repr(s.strip()))
# print(repr(s.lstrip()))   # 这行在干嘛:去掉左边空白
print(repr(s.lstrip()))
# print(repr(s.rstrip()))   # 这行在干嘛:去掉右边空白
print(repr(s.rstrip()))
# print(repr(s.strip(" H")))# 这行在干嘛: (参数是"字符集合", 不是"字符串") 去掉所有H和空白
print(repr(s.strip(" H")))
# print(repr(s.upper()), repr(s.lower()))
print(repr(s.upper()),repr(s.lower()))  # 把s进行大写和小写转换后再显形空格和换行符
# print(repr(s.find("World")), s.count("l"), s.startswith("H"))
print(repr(s.find("World")),s.count("l"), s.startswith("H")) # 检查s里面有没有World字符串,有几个l,是不是以H开头

# --- A 组 8 题 -----------------------------------------------------
# 提示: 每题 print 一行分隔线, 例如 print("\n--- A1 ---")

# A1 打印 repr(s) / repr(s.strip()) / repr(s.lstrip()) / repr(s.rstrip())
print("\n--- A1 ---")
# 你的代码 ↓
print(repr(s))
print(repr(s.strip()))
print(repr(s.lstrip()))
print(repr(s.rstrip()))
# A2 把 fruit_text 切成列表并打印长度; 再只切 1 次, 对比两次结果
print("\n--- A2 ---")
# 你的代码 ↓
print(len(fruit_text.split(",")))
print(len(fruit_text.split(",",1)))
# A3 把 names_for_join 用 "、" join 成一行
print("\n--- A3 ---")
# 你的代码 ↓
print("、".join(names_for_join))

# A4 把 numbers_for_join 用 "-" join: 先让它报错一次(抄报错), 再用 str() 修好
print("\n--- A4 ---")
# 你的代码 ↓
try:
   print("-".join(numbers_for_join))
except TypeError:
   print("TypeError: sequence item 0: expected str instance, int found")
print("-".join(str(x) for x in numbers_for_join))
# A5 把 dash_text 里的 - 换成 +, 然后打印 dash_text, 验证它没变
print("\n--- A5 ---")
# 你的代码 ↓
dash_text.replace("-","+")
print(dash_text)

# A6 hello 转全大写、全小写, 各打印一次
print("\n--- A6 ---")
# 你的代码 ↓
print(hello.upper())
print(hello.lower())

# A7 判断 filename 是否以 test_ 开头、以 .py 结尾
print("\n--- A7 ---")
# 你的代码 ↓
print(filename.startswith("test_"))
print(filename.endswith(".py"))

# A8 统计 sentence 里 l 的次数; 找 "world" 的下标; 再找一个不存在的词看 find 返回什么
print("\n--- A8 ---")
sentence = "hello world"          # A8

# 你的代码 ↓
print(sentence.count("l"))
print(sentence.find("world"))
print(sentence.find("hxc"))
# ======================================================================
# B 区 · 文件读写(上午)  —— 文件名和内容已给好
# ======================================================================
DEMO_FILE = "demo.txt"
DEMO_LINES = ["第一行\n", "第二行\n"]   # B1 要写进文件的两行

# B1 用 "w" + with 把 DEMO_LINES 写进 DEMO_FILE (encoding="utf-8")
#    提示: for line in DEMO_LINES: f.write(line)
#    写完用 VS Code 打开 demo.txt 肉眼确认
print("\n--- B1 ---")
# 你的代码 ↓
with open(DEMO_FILE,"w",encoding="utf-8") as f:
   for line in DEMO_LINES:
      f.write(line)

# B2 用 read() 读成一个大字符串, 打印 repr(内容)  ← 用 repr 才看得见 \n
print("\n--- B2 ---")
# 你的代码 ↓
with open(DEMO_FILE,encoding="utf-8") as f:
   s=f.read()
print(repr(s))

# B3 用 readlines() 读成列表, 打印; 再逐行 for, 每行打印 repr
print("\n--- B3 ---")
# 你的代码 ↓
with open(DEMO_FILE,encoding="utf-8") as f:
   s=f.readlines()
print(s)
for i in s:
   print(repr(i))

# B4 用 "a" 追加第三行 "第三行\n", 重新读, 确认前两行还在
print("\n--- B4 ---")
# 你的代码 ↓
with open(DEMO_FILE,"a",encoding="utf-8") as f:
   f.write("第三行\n")
with open(DEMO_FILE,encoding="utf-8") as f:
   s=f.read()
print(repr(s))   

# B5 用 "w" 写一行 "只剩这行\n", 重新读, 亲眼看到前面的被清空了
print("\n--- B5 ---")
# 你的代码 ↓
with open(DEMO_FILE,"w",encoding="utf-8") as f:
   f.write("只剩这行\n")
with open(DEMO_FILE,encoding="utf-8") as f:
   s=f.read()
print(repr(s))
# B6 试着 open("不存在的文件.txt") 让它崩, 把报错抄在下面, 再用 try/except 修好
# 报错:
print("\n--- B6 ---")
# 你的代码 ↓
try:
   open("不存在的文件.txt",encoding="utf-8")
except FileNotFoundError:
   print("FileNotFoundError: [Errno 2] No such file or directory: '不存在的文件.txt'")

# ======================================================================
# E 区 · 故意写错 5 条(全部用 try/except 包住, 让脚本能跑完)
# ======================================================================
# E1 open("不存在.txt")  → FileNotFoundError
#    报错:FileNotFoundError: [Errno 2] No such file or directory: '不存在.txt'
#    原因:打开了一个不存在的文件
#
# E2 "w" 模式清空内容(不是报错, 是数据没了) —— 这个最危险
#    现象:只剩新写的内容,原来内容都不见了
#    原因:"w" 模式会清空以前内容
#
# E3 "-".join([1, 2, 3])  → TypeError
#    报错:TypeError: sequence item 0: expected str instance, int found
#    原因:join 只能连接字符,不能连整型
#
# E4 sum(读回来的行)  → TypeError
#    报错:TypeError: unsupported operand type(s) for +: 'int' and 'str'
#    原因:读回来的行中有字符串,不能将字符串与整型相加
#
# E5 写中文不写 encoding, 读时写 utf-8  → UnicodeDecodeError
#    报错:UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb5 in position 0: invalid start byte
#    原因:和Python的默认编码冲突


# ======================================================================
# C 区 · 实战 T1-T7(不看教程)  —— 数据已给好
# ======================================================================

# ---------------- T1 / T2 用这份数据 ----------------
raw_line = "  张三,85,  数学  "

# T1 清洗这一行, 输出 ['张三', '85', '数学']
#    步骤: strip() 去两端空白 → split(",") 拆开 → 每一段再 strip()
#    提示: [x.strip() for x in raw_line.strip().split(",")]
print("\n--- T1 ---")
# 你的代码 ↓
s=[x.strip() for x in raw_line.strip().split(",")]
print(s)
# 为什么我这样写输出的结果不对??
s=[x.strip() for x in raw_line.strip().split(",")]
print(s)
# T2 把 T1 的结果用 " | " join 成一行, 输出 张三 | 85 | 数学
print("\n--- T2 ---")
# 你的代码 ↓
print(" | ".join(s))

# ---------------- T3 用这份数据 ----------------
score_text = "92"

# T3 转成 int, 判断是否及格(>=60), 打印 "92 及格"
#    再试 int("九十二"), 把报错抄进注释
print("\n--- T3 ---")
# 你的代码 ↓
if int(score_text) >= 60:
   print(score_text+" 及格")
# int("九十二") 报错:ValueError: invalid literal for int() with base 10: '九十二'

# ---------------- T4 用这份数据 ----------------
lines_data = ["张三,85\n", "李四,92\n", "王五,78\n"]

# T4 这就是"从文件读出来的样子"(每行带 \n)。要求:
#    1) 逐行 strip() 去换行 → split(",") 拆开 → 转成 {"name": ..., "score": ...}
#    2) 得到 3 条的 dict 列表
#    3) 打印每个人 + 平均分(保留 1 位小数)
print("\n--- T4 ---")
# 你的代码 ↓
ans={}

for i in lines_data:
   i = i.strip().split(",")
   ans[i[0]]=i[1]
print(ans)   
total = 0
for i in ans.values():
   total+=int(i)
print(f"平均分:{total/len(ans)}")
# ---------------- T5 / T6 / T7 用 scores.txt ----------------
SCORES_FILE = "scores.txt"

# T5 把 T4 的结果写进 scores.txt, 一行一条: 张三,85
#    要求: with open(..., "w", encoding="utf-8"); 每条自己加 \n
#    写完用 VS Code 打开文件肉眼确认
print("\n--- T5 ---")
# 你的代码 ↓
with open("scores.txt", "w", encoding="utf-8") as f:
   for i,j in ans.items():
      f.write(i + "," +j+"\n")

# T6 用 readlines() 读回 scores.txt, 打印列表; 用 repr 看每行末尾的 \n
print("\n--- T6 ---")
# 你的代码 ↓
with open("scores.txt", encoding="utf-8") as f:
   s=f.readlines()
print(s)
# 不用repr好像也能看到每行末尾的 \n

# T7 两步, 都要做:
#    ① 用 "a" 追加一条 "赵六,88", 重新读, 确认前 3 条还在
#    ② 用 "w" 写一条新内容, 重新读, 亲眼看到前面的被清空了
print("\n--- T7 ---")
# 你的代码 ↓
with open("scores.txt", "a", encoding="utf-8") as f:
   f.write("赵六,88\n")
with open("scores.txt", encoding="utf-8") as f:
   s=f.readlines()
print(s)
with open("scores.txt", "w", encoding="utf-8") as f:
   f.write("赵六,88\n")
with open("scores.txt", encoding="utf-8") as f:
   s=f.readlines()
print(s)