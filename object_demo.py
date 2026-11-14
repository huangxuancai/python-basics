# -*- coding: utf-8 -*-
"""
概念演示：实例 / 变量 / 方法 / __str__ 的关联
================================================
用法:  python object_demo.py
这是 todo.py 的最小骨架版，每一步只演示一个概念。
改着玩：把任何一步的注释解开/改掉，重跑看结果变化。
"""

# ========== 第 1 步：类只是模板 ==========
class Todo:
    def __init__(self, title):
        self.title = title        # 实例属性：每个实例自己的
        self.done = False

    def mark_done(self):          # 方法：定义在模板里的"能力"
        self.done = True

    def __str__(self):            # 打印我时长什么样
        mark = "[x]" if self.done else "[ ]"
        return f"{mark} {self.title}"

print("第1步  Todo 本身 =", Todo)
print("       ← 这只是模板，还没有任何实例存在")

# ========== 第 2 步：造实例 ==========
a = Todo("复习列表")
print("\n第2步  a =", a)
print("       type(a) =", type(a).__name__)
print("       a.title =", a.title)
print("       ← Todo('复习列表') 按模板造出一个实例，a 是指向它的标签")

# ========== 第 3 步：变量只是标签，赋值不复制 ==========
b = a
print("\n第3步  b = a 之后，b is a ?", b is a)
b.title = "改了标题"
print("       改 b.title 之后，a.title =", a.title)
print("       ← b 和 a 是同一个实例的两张标签，改谁都是改同一个东西")

# ========== 第 4 步：两个实例互不影响 ==========
c = Todo("写代码")
print("\n第4步  c is a ?", c is a)
c.mark_done()
print("       c 标记完成后: c =", c)
print("       a 没被影响:    a =", a)
print("       ← 每次 Todo(...) 都是新实例，各改各的，靠 self 区分")

# ========== 第 5 步：列表装的是实例本身（引用），不是复制 ==========
todos = [a, c]
print("\n第5步  todos[0] is a ?", todos[0] is a)
print("       todos[1] is c ?", todos[1] is c)
print("       ← 列表里装的就是那两个实例，没有复制")

# ========== 第 6 步：for 循环变量 = 每圈重新贴标签 ==========
for i, todo in enumerate(todos, start=1):
    print(f"\n第6步 第{i}圈: todo is todos[{i-1}] ?", todo is todos[i-1])
    print(f"       f'{{i}}. {{todo}}' → {i}. {todo}")
print("       ← todo 不是单独声明的，for 那一行就是声明处，每圈绑定到当前元素")

# ========== 第 7 步：print(列表) 为什么是地址 ==========
print("\n第7步  print(todos) →", todos)
print("       ← 列表打印用元素的 __repr__，我们只写了 __str__，所以显示默认地址")
print("       对比逐个打印:")
for t in todos:
    print("       ", t, " ← 单个对象走 __str__")

# ========== 第 8 步：映射回 todo.py ==========
print("\n第8步  你的 todo.py 里:")
print("       load_todos()          = 批量执行第2步（从文件每行造一个实例）")
print("       todos                 = 第5步的列表")
print("       for i, todo in ...    = 第6步")
print("       f'{i}. {todo}'        = 触发 __str__")
print("       todos[i].mark_done()  = 第4步的方法调用")
