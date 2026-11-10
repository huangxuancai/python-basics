# -*- coding: utf-8 -*-
"""
W1 Day4 · 列表与字典 练习骨架
================================================
用法:  python day4_practice.py
规则:  1) 每写完 3-5 行就运行一次, 不要一次写完再跑
       2) 报错只读最后一行, 抄进注释, 写一句中文原因
       3) 禁止截图, 笔记就是这里的注释
讲义:  C:\\Users\\-\\Desktop\\project_Job-Hunt_20251108_v1.0\\02-学习内容\\05-W1Day4-列表与字典.md

分区:
  A 区  列表 12 个操作 + 8 道题      (09:00-10:30)
  B 区  切片 5 道题                  (10:30 前后)
  E 区  故意写错的 5 条, 报错抄这里    (下午任意时间)
  C 区  实战 T1-T8, T8 是今天的主产出  (14:00-16:30)
"""

# ======================================================================
# 0 · 开场自测(不查资料, 先把答案写在下面, 写完再往下看讲义)
# ======================================================================
# 1. 空列表 / 三元素列表:
# 答:[]/ [1,2,3]
# 2. 往末尾加元素:
# 答:apepend
# 3. 第 1 个 / 最后 1 个元素的下标:
# 答:0,len-1
# 4. len([1, 2, 3]) =
# 答:3
# 5. 取出字典所有 key 的方法:
# 答:idont know


# ======================================================================
# A 区 · 列表基础(09:00-10:30)
# ======================================================================
# --- 12 个操作: 每个都敲一遍, 敲完注释一句"这行在干嘛"
# nums = [3, 1, 4, 1, 5]
nums = [3,1,4,1,5] # 给列表赋值
# nums.append(9)
nums.append(9)  #在列表的末尾加上一个9
# nums.insert(0, 100)
nums.insert(0,100) #在列表下标为0的位置上插入100
# nums.extend([7, 8])
nums.extend([7,8]) #在列表的末尾加入7,8两个元素
# nums.remove(1)
nums.remove(1) #去掉值第一个为1的元素
# nums.pop()
nums.pop() #弹出列表最后一个元素
# nums.pop(0)
nums.pop(0) #弹出下标为0的元素
# print(len(nums), sum(nums), max(nums), min(nums))
print(len(nums),sum(nums),max(nums),min(nums)) #打印列表的长度,和,最大值,最小值
# print(nums.index(4), 4 in nums, nums.count(1))
print(nums.index(4),4 in nums,nums.count(1)) #打印列表值为4的下标,4是否在列表中,列表中值为1的个数


# --- A 组 8 题 -----------------------------------------------------
# A1 建列表 [85, 92, 78, 92, 60], 打印长度/总和/最大值/最小值
nums1=[85, 92, 78, 92, 60]
print(len(nums1),sum(nums1),max(nums1),min(nums1))

# A2 末尾加 100, 第 0 位插 50, 打印列表
nums1.append(100)
nums1.insert(0,50)
print(nums1)

# A3 删掉第一个 92, 再删掉最后一个元素, 打印列表
nums1.remove(92)
nums1.pop()
print(nums1)

# A4 判断 60 在不在列表里; 打印 92 出现了几次
print(60 in nums1,nums1.count(92))

# A5 从小到大排并打印; 再从大到小排并打印
nums1.sort()
print(nums1)
nums1.sort(reverse=True)
print(nums1)

# A6 用 sorted 得到新列表, 验证原列表没变
nums2=[50, 85, 78, 92, 60]
print(sorted(nums2))
print(nums2)

# A7 打印前两个、后两个元素(切片)
print(nums2[:2])
print(nums2[-2:])

# A8 用 [0]*5 建列表, 把第 2 个改成 99, 打印
nums3=[0]*5
nums3[1]=99
print(nums3)

# ======================================================================
# B 区 · 切片(5 题)
# ======================================================================
# data = [10, 20, 30, 40, 50, 60]
data = [10, 20, 30, 40, 50, 60]
# B1 前 3 个 / 后 3 个
print(data[:3])
print(data[-3:])
# B2 取 [20, 30, 40]
print(data[1:4])

# B3 取所有偶数位(下标 0, 2, 4)
print(data[::2])

# B4 [::-1] 反转 与 reverse() 反转, 对比
print(data[::-1])
print(data.reverse())
'''
要新列表、不改原数据 → 用 [::-1]

要原地反转、省内存 → 用 .reverse()，但别直接 print 它
'''

# B5 先故意写 data[100] 让它崩, 把报错最后一行抄在下面, 再改 data[100:] 确认不崩
# 报错:IndexError: list index out of range


# ======================================================================
# E 区 · 故意写错 5 条(报错抄进注释, 每条后面写中文原因)
# ======================================================================
# E1 nums[100]
# 报错:IndexError: list index out of range
# 原因:下标超出范围
#
# E2 nums["a"]
# 报错:list indices must be integers or slices, not str
# 原因:列表下标必须是整型或者切片,不能是字符
#
# E3 scores["不存在的人"]
try:
    {"张三": 85}["不存在的人"]
except KeyError as e:
    print("E3 →", type(e).__name__ + ":", e)
# 报错: KeyError
# 原因: 
#
# E4 遍历字典时 pop  
dd = {"a": 1, "b": 2}
try:
    for k in dd:
        dd.pop(k)
except RuntimeError as e:
    print("E4 →", type(e).__name__ + ":", e)
# 报错:
# 原因:"崩在取下一个元素时""加已有 key 不算改大小"
#
# E5 result = nums.sort() 后 print(result)
result = nums.sort()
print(result)
# 输出:None
# 原因:nums.sort() 是列表的原地排序方法，它直接修改 nums 本身，返回值是 None。所以 result 得到的是 None，而不是排序后的列表。


# ======================================================================
# C 区 · 实战 T1-T8(不看教程)
# 下面是每题的数据, 已经给好, 不要改、不要重抄; 你在 "你的代码 ↓" 下面写逻辑
# ======================================================================

# ---------------- T1 / T2 用这份数据 ----------------
scores = [85, 92, 78, 92, 60]

# T1 打印总分、平均分(保留 1 位小数)、最高分、最低分
print("\n--- T1 ---")
# 你的代码 ↓
print(sum(scores),round(sum(scores)/len(scores),1),max(scores),min(scores))

# T2 从高到低排, 用切片打印前三名(不要动 scores 本身)
print("\n--- T2 ---")
# 你的代码 ↓
print(sorted(scores,reverse=True)[:3])

# ---------------- T3 用这份数据 ----------------
raw_scores = [85, 92, 78, 92, 60, 85]

# T3 去重且保持原顺序, 打印结果
#   写法① 循环 + not in
#   写法② dict.fromkeys()
print("\n--- T3 ---")
# 你的代码 ↓
answer1=[]
for i in raw_scores:
    if i not in answer1:
        answer1.append(i)
print(answer1)

answer2=list(dict.fromkeys(raw_scores))
print(answer2)

# ---------------- T4 用这两份数据 ----------------
names = ["张三", "李四", "王五"]
scores_part = [85, 92, 78]

# T4 合成字典 {"张三": 85, "李四": 92, "王五": 78}
#   先 for + 下标; 再试 dict(zip(names, scores_part))
print("\n--- T4 ---")
dict1={}
# 你的代码 ↓
for i in range(len(names)):
    dict1[names[i]]=scores_part[i]
print(dict1)
dict2=dict(zip(names,scores_part))
print(dict2)
# ---------------- T5 用这份数据 ----------------
score_map = {"张三": 85, "李四": 92, "王五": 78}

# T5 按分数从高到低排序, 打印排名
#   照抄下面这行, 跑通, 然后在注释里用中文讲清每个部分:
#   ranking = sorted(score_map.items(), key=lambda x: x[1], reverse=True)
print("\n--- T5 ---")
# 你的代码 ↓
ranking = sorted(score_map.items(),key=lambda x:x[1],reverse=True)
print(ranking)
#sorted用来比较,items拿出元组,key接受函数作用于列表的所有元素,用函数返回值作为排序依据,lambda匿名函数,reverse=True降序

# ---------------- T6 用这份数据 ----------------
sentence = "the quick brown fox jumps over the lazy dog the fox"

# T6 统计每个单词出现次数, 输出前 3 名
#   提示: 出现次数相同的词谁排前面没有保证, 验证"次数对不对"就行
print("\n--- T6 ---")
# 你的代码 ↓
word = sentence.split()
times = {}
for w in word:
    times[w] = times.get(w,0)+1
top3 = sorted(times.items(), key=lambda kv: kv[1], reverse=True)[:3]
print(top3)


# ---------------- T7 用这份数据 ----------------
student_names = ["张三", "李四", "王五"]
matrix = [
    [85, 92, 78],   # 张三
    [60, 70, 65],   # 李四
    [95, 88, 91],   # 王五
]

# T7 打印每个人的总分(嵌套 for: 外层取人, 内层取分数)
#   提示: 用下标 i 把 student_names[i] 和 matrix[i] 对上
print("\n--- T7 ---")
# 你的代码 ↓
for i in range(len(student_names)):
    total=0
    for j in range(len(matrix[i])):
        total+=matrix[i][j]
    print(total)
# ---------------- T8 ⭐ 主产出 ----------------
#   这两条只是测试数据, 用来验证"列出 / 标记完成 / 删除"能不能跑
todos = [
    {"title": "复习列表", "done": False},
    {"title": "复习字典", "done": True},
]

# T8 list of dict 待办清单
#   菜单: 1 添加 / 2 列出 / 3 标记完成 / 4 删除 / q 退出
#   要求: 编号从 1 开始; 已完成显示 [x], 未完成显示 [ ]; 输入 abc 不崩
#   验收: 加 2 条 → 列出 → 标记第 1 条完成 → 再列出 → 删除第 2 条 → 再列出 → q
print("\n--- T8 ---")
# 你的代码 ↓
while True:
    print("1 添加")
    print("2 列出")
    print("3 标记完成")
    print("4 删除")
    print("q 退出")
    choice=input("请输入你的选项:")
    if choice == "1":
        add_title=input("请输入你需要添加的代办事项:")
        todos.append({"title":add_title,"done":False})
        print("================================")
    elif choice == "3":
        if not todos:
          print("暂无事项可操作")
          continue
        temp=input("请输入你已完成的事项编号:")
        try:
            finish_index=int(temp)
        except ValueError:
            print("输入无效，请输入数字")
            continue
        finish_index-=1
        if finish_index >= len(todos) or finish_index < 0:
            print("输入编号无效!")
            continue
        todos[finish_index]["done"]=True
        print("已标记完成")
        print("================================")
    elif choice == "4":
        if not todos:
          print("暂无事项可操作")
          continue
        temp=input("请输入你要删除的事项编号:")
        try:
            del_index=int(temp)
        except ValueError:
            print("输入无效，请输入数字")
            continue
        del_index-=1
        if del_index >= len(todos) or del_index < 0:
            print("输入编号无效!")
            continue
        todos.pop(del_index)
        print("已删除")
        print("================================")
    elif choice == "2":
        if not todos:
              print("暂无事项可操作")
              continue
        else: 
            for i,todo in enumerate(todos,start=1):
                mark="[x]" if todo["done"] else "[ ]"
                print(f"{i}. {mark} {todo['title']}")
        print("================================")
    elif choice == "q":
        break
    else:
        print("输入有误,请重新输入!")
        print("================================")