# -*- coding: utf-8 -*-
"""
W2 Day2 · 类与对象练习（数据全部已给好，你只写类和逻辑）
================================================
用法:  python day8_practice.py
规则:  1) 每题下面有 "# 期望输出:",写完跑一次对答案
       2) 不许改上面的数据
       3) 卡住先看讲义: 02-学习内容/11-W2Day2-类与对象.md

分区:
  A 区 6 题  类的基础：__init__ / 实例方法 / __str__ / 类属性 / self
  B 区 5 题  继承：super / 方法覆盖 / isinstance
  C 区 5 题  实战小类：Student / BankAccount
  D 区       ⭐ 主产出：新建 todo_class.py（不在本文件写）

⚠️ 类名首字母大写；方法第一个参数必须是 self
"""

# ======================================================================
# 0 · 开场自测(不查资料)
# ======================================================================
# 1. 定义类用什么关键字:
# 答:class
# 2. __init__ 什么时候被调用:
# 答:初始化时
# 3. self 指什么:
# 答:调用者本身
# 4. 类属性和实例属性写的位置有什么区别:
# 答:类属性写在class下.实例属性在self.后面
# 5. 子类怎么调用父类的 __init__:
# 答:super()


# ======================================================================
# A 区 · 类的基础(6 题)
# ======================================================================
print("\n=== A 区 ===")

# A1 定义 Todo 类:__init__(self, title, done=False) 存两个属性
#    创建 Todo("复习类") 和 Todo("写代码", done=True),打印它们的属性
# 期望输出: 复习类 False   然后   写代码 True
# 你的类 ↓

class Todo:
    def __init__(self,title,done = False):
        self.title=title
        self.done = done 

    def mark_done(self):
        self.done=True

    def __str__(self):
        mark = "[x]" if self.done else "[ ]"
        return (f"{mark} {self.title}") 
        
t1=Todo("复习类")
t2=Todo("写代码", done=True)
print("A1",t1.title,t1.done )
print("A1",t2.title,t2.done )


# A2 给 Todo 加 mark_done() 方法(把 self.done 改成 True)
#    创建一个,调 mark_done(),打印 done
# 期望输出: True
# 你的代码 ↓
t3=Todo("吃饭")
t3.mark_done()

print("A2", t3.done)


# A3 给 Todo 加 __str__:返回 "[ ] 标题" 或 "[x] 标题"
#    打印 Todo("复习类")
# 期望输出: [ ] 复习类
# 你的代码 ↓


print("A3", Todo("复习类"))


# A4 创建两个 Todo,只标记第一个完成,打印两个的 done 验证互不影响
# 期望输出: True False
# 你的代码 ↓
t4=Todo("完成",done=True)
t5=Todo("未完成")

print("A4",t4.done,t5.done )


# A5 定义 Counter 类:类属性 count=0,每次 __init__ 让 Counter.count += 1
#    并把当前值存进 self.id。创建 3 个,打印各自的 id 和 Counter.count
# 期望输出: 1 2 3   然后   3
# 你的类 ↓
class Counter:
    count=0
    def __init__(self,id):
        Counter.count+=1
        self.id=Counter.count

a=Counter("a")
b=Counter("b")
c=Counter("c")
print("A5", a.id,b.id,c.id)
print("A5 Counter.count =",Counter.count )


# A6 故意写一个类,里面的 hello() 不写 self;创建实例调用它
#    把报错抄进注释
# 报错:TypeError: Guyi.hello() takes 0 positional arguments but 1 was given
# 你的代码 ↓
class Guyi:
    def hello():
        return "hi"
try:
    Guyi().hello()
except TypeError:
    print("TypeError: Guyi.hello() takes 0 positional arguments but 1 was given")

# ======================================================================
# B 区 · 继承(5 题)
# ======================================================================
print("\n=== B 区 ===")

# B1 定义 TimedTodo(Todo):__init__(self, title, due)
#    用 super().__init__(title) 调父类,再存 self.due
#    创建 TimedTodo("交作业", "11-20"),打印 title 和 due
# 期望输出: 交作业 11-20
# 你的类 ↓
class TimedTodo(Todo):
    def __init__(self, title, due):
        super().__init__(title)
        self.due = due

    def __str__(self):
        return  f"{super().__str__()} (截止 {self.due})"
t6=TimedTodo("交作业", "11-20")
print("B1",t6.title,t6.due )


# B2 给 TimedTodo 重写 __str__:在父类 __str__ 基础上加 " (截止 xx)"
#    打印它
# 期望输出: [ ] 交作业 (截止 11-20)
# 你的代码 ↓


print("B2", t6)


# B3 对 B1 那个实例调父类的 mark_done(),再打印
# 期望输出: [x] 交作业 (截止 11-20)
# 你的代码 ↓
t6.mark_done()

print("B3",t6 )


# B4 三个对比检查(用 B1 的 t6 当子类实例,再建一个普通 Todo 当对照)
#    ① isinstance(t6, Todo)            子类实例算不算父类类型?
#    ② isinstance(普通Todo, TimedTodo)  反过来成不成立?
#    ③ type(t6) is Todo                精确类型是不是 Todo?
# 期望输出: True False False
# 你的代码 ↓


print("B4",isinstance(t6, Todo),isinstance(Todo("随便"), TimedTodo),type(t6) is Todo )


# B5 故意写一个子类,__init__ 里【不调】super().__init__(),只存自己的属性
#    然后访问继承来的属性(title),把报错抄进注释
# 报错:
# 你的代码 ↓
class CleanTodo:
    def __init__(self, title):
        self.title = title

class BadTimed(CleanTodo):
    def __init__(self, title, due):
        # 故意不调 super().__init__(title)
        self.due = due

try:
    b = BadTimed("交作业", "11-20")
    print(b.title)
except AttributeError as e:
    print("B5", type(e).__name__ + ":", e)


# ======================================================================
# C 区 · 实战小类(5 题)
# ======================================================================
print("\n=== C 区 ===")

# C1 定义 Student 类:name / score;加 is_pass(line=60) 方法返回布尔
#    创建 Student("张三", 85),打印 is_pass() 和 is_pass(90)
# 期望输出: True False
# 你的类 ↓
class Student:
    def __init__(self,name,score):
        self.name=name
        self.score=score

    def is_pass(self,line=60):
        return self.score > line

    def __str__(self):
        mark = "(及格)" if self.score >= 60 else "(不及格)"
        return f"{self.name}: {self.score} {mark}"    
s1=Student("张三", 85)
print("C1", s1.is_pass(),s1.is_pass(90))


# C2 给 Student 加 __str__:输出 "张三: 85 (及格)" 这种(不及格就写"不及格")
# 期望输出: 张三: 85 (及格)
# 你的代码 ↓


print("C2", s1)


# C3 用下面的 students_c 建一个 Student 列表,按分数从高到低排序,打印每个的 str
# 期望输出: 李四: 92 (及格) / 张三: 85 (及格) / 王五: 78 (及格)
students_c = [("张三", 85), ("李四", 92), ("王五", 78)]
# 你的代码 ↓
s_list=[]
for s in students_c:
    s_list.append(Student(*s))
ranked=sorted(s_list,key=lambda s:s.score,reverse=True)
for r in ranked:
    print(r,end=" / ")

print("\n")
# C4 定义 BankAccount 类:balance(初始 0)
#    deposit(x) 加钱返回新余额;withdraw(x) 扣钱,余额不足抛 ValueError
#    测试:存 100,取 30,取 1000(应抛异常并用 try/except 捕获)
# 期望输出: 100 70 然后 ValueError: 余额不足
# 你的类 ↓
class BankAccount:
    total_accounts=0
    def __init__(self):
        self.balance=0
        BankAccount.total_accounts+=1
    
    def deposit(self,x):
        self.balance+=x
        return self.balance
    
    def withdraw(self,x):
        if self.balance - x < 0:
            raise ValueError("余额不足")
        else:
            self.balance-=x
            return self.balance
      
a=BankAccount()
print("C4", a.deposit(100),a.withdraw(30))
try:
    a.withdraw(1000)
except ValueError as e:
    print("C4", type(e).__name__ + ":", e)

# C5 给 BankAccount 加类属性 total_accounts,每次 __init__ 自增
#    创建 2 个账户,打印 BankAccount.total_accounts
# 期望输出: 2
# 你的代码 ↓
b=BankAccount()

print("C5", BankAccount.total_accounts)


# ======================================================================
# D 区 · ⭐ 主产出：新建 todo_class.py（不在本文件写）
# ======================================================================
# 复制 todo.py 的骨架,把 list of dict 改成 list of Todo 对象。
#
# class Todo:
#     __init__(self, title, done=False)
#     mark_done(self)
#     to_line(self)          -> "标题,0/1"
#     from_line(cls, line)   -> Todo 对象（@classmethod 照抄即可）
#     __str__(self)          -> "[x] 标题" / "[ ] 标题"
#
# 替换点:
#   load_todos()   -> [Todo.from_line(l) for l in lines ...]
#   save_todos()   -> f.write(t.to_line() + "\n")
#   print_todos()  -> print(f"{i}. {todo}")     ← 靠 __str__
#   标记完成        -> todos[idx].mark_done()
#   show_stats()   -> sum(1 for t in todos if t.done)
#
# 验收: 跑一遍 加/列/标/删/重启,输出和 todo.py 完全一样
