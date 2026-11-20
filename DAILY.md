# 每日复盘

> 规则：每天 20:00-21:00 的最后 10 分钟写一节，写完就 commit。
> 只写「卡在哪 + 怎么解的」，**不抄知识点、不写流水账、不写感受**。
> 模板与红线见 `find-job/11_每日复盘模板.md`。

---

## 2026-11-08（W0 前置 Day）

**做了什么**：装环境、hello.py、guess.py 猜数字游戏

**卡住的地方**
1. VS Code 里改了代码，`git status` 却报 `working tree clean`，以为 git 坏了
2. 次数上限写的是 `if count > 7`，测出来实际能猜 8 次

**怎么解的**
1. 搞清了一件事：**git 只认磁盘上已保存的文件**，VS Code 里改完没按 Ctrl+S，磁盘上还是老内容，git 自然看不到。以后改完先看标签页有没有白点
2. 写了个小脚本模拟循环次数，验证出 `count > 7` 会跑 8 次、`count >= 7` 才是 7 次。原因是判断放在循环**开头**，那时 count 还没 +1

**面试能用**：问"你遇到过什么 bug"，我可以讲这个 off-by-one，并且能说清"为什么靠功能测试很难发现，必须专门设计边界用例"

**明天第一件事**：给 guess.py 加 try/except，让输入 `abc` 不崩溃

---

## 2026-11-08（W0）· 知识盘点测试 T1

不看资料，5 题自测，结果留档用于三个月后对比：

| # | 题目 | 我的答案 | 评级 |
|---|---|---|---|
| 1 | Java 定义类的语法 | 忘了 | ❌ |
| 2 | C 指针是什么 | 变量的存储位置 | 🟡 差一层：指针是存**地址的变量** |
| 3 | list 和 dict 的区别 | 不知道（但 test.py 里用过） | ❌ |
| 4 | 梯度下降干什么的 | 减少误差？ | 🟡 缺"沿梯度反方向更新参数" |
| 5 | 写一段完整代码 | 只有 guess.py | ✅ |

**结论**：5 题里 1 题完整、2 题半对、2 题不会。

唯一能完整写出来的代码，是唯一亲手敲过、亲手改过 bug 的代码。
上百小时看视频 → 0 行留存；40 分钟动手 → 18 行完整留存。

**补上的**：`nums[0]` 按下标取，`ages.get("张三")` 按 key 取。
`ages["不存在"]` 会 KeyError 崩溃，`ages.get("不存在")` 返回 None 不崩 —— 这就是"防御式编程"，明天 try/except 的核心。

---

## 2026-11-09（W1 Day2）

**做了什么**：给 guess.py 加了非法输入校验和重玩功能

**卡住的地方**:

```
1. `break` 写在了 try 里面，以为能跳出"重新输入"，结果跳出了整个主循环——输对数字程序直接结束
2. `raw = input()` 写在内层 while 外面，输 abc 后死循环，3 秒刷了 100 万行
```

**怎么解的**:

```
1. 在外面加一层 while 专门管输入，`break` 放进去，跳的是内层
2. input 移进内层 while，每轮重新读
```

**学到的规律**：

```
- break 只跳最近一层循环
- while 要退出的条件里，涉及的变量必须在循环体内被更新，否则死循环
```

**面试能用**：问"你遇到过什么 bug"，可以讲这两个，并说清"测非法输入是默认动作"

**明天第一件事**：W1 Day3，if/for/while 综合，做 todo.py 的雏形

---

## 2026-11-09（W1 Day3）

**做了什么**：`for` + `range` 五道练习（打印偶数、1-100 求和、九九乘法表、列表元素平方、字符统计），全部跑通

**卡住的地方**：
```
第 5 题（统计 "hello world" 里每个字符出现次数）完全不知道从哪下手。
不是逻辑不懂，是不知道"怎么把值存进字典"——昨天只学了取值，没学存值。
```

**怎么解的**：
```
退回去补了字典的写操作，分 6 步跑：
1. maps["dust2"] = 1            → 新增一个键值对
2. maps["dust2"] = 99           → 覆盖/修改（和新增是同一个语法）
3. maps["nuke"]                 → KeyError 崩溃
4. if "nuke" in maps: ... else: ...   → 先判断存在性
5. maps.get("nuke", 0) + 1      → 第 3、4 步的简化版
6. 循环里重复第 5 步             → 这就是"计数"
看懂之后，第 5 题就是 count[c] = count.get(c, 0) + 1，一行搞定
```

**学到的规律**：
```
- d[key] = value 这一行：key 不存在是新增，存在是覆盖。Python 不区分这两个动作
- 计数模式 = 字典 + get(key, 0) + 1。以后统计用例通过数、日志错误数，全是这个
- 变量遮蔽：sum = 0 会覆盖内置的 sum() 函数，之后 sum([1,2,3]) 会 TypeError。
  内置名不能当变量名：sum / list / dict / max / min / input / type / id / len
```

**面试能用**：
- "字典计数"这个模式，以及 `d.get(k,0)+1` 和 `if k in d` 两种写法的区别
- 被问"你的代码有什么可以改进的"，可以讲变量遮蔽这个问题

**明天第一件事**：W1 Day4，列表与字典（列表的增删改查、遍历、切片；字典的 `items()` 遍历）

---

## 2026-11-10（W1 Day4）

**做了什么**：`day4_practice.py` 全部跑通（A1-A8 列表操作、B1-B5 切片、T1-T7 统计/去重/合成字典/词频/二维列表）；T8 用 `list of dict` 写出待办清单，含添加/列出/标记完成/删除，外加越界检查和 `ValueError` 校验

**卡住的地方**：

```
1. sort() 返回 None 我一天踩两次：E5 里已经写清"返回值是 None"，T2 手又写成 print(scores.sort(reverse=True))，
   结果 T2 打印 None，还把 scores 原地改成了降序（题目要求"不要动 scores"）
2. E4 我以为"遍历时删就必崩"，实际规则是"元素个数变了才崩"：
   改 value 不崩、加已有 key 也不崩（只是覆盖）、加新 key 才崩
3. for k in dd 里 k 是 key（字符串），dd[k] 是 value（数字）。
   我把 dd[k] 当成字符串，判断"dd[k]+1 会崩"，判反了
4. B5 我跑的是 data[100:]（切片，返回 [] 不报错），却把 data[100]（索引，报 IndexError）的报错抄进注释。
   结论是抄来的，没真撞过
5. enumerate(todos, start=1) 时 i 是"显示编号"，不是下标。写 todos[i] 第一圈就已经错位（取到第 2 条），
   第二圈才 IndexError
```

**怎么解的**：

```
1. 5 条报错全部改成 try/except + print(type(e).__name__, e)，
   让报错由程序打出来，而不是我背下来
2. 逐条实测边界，不靠推理：改 value 不崩 / 加新 key 崩 / 加已有 key 不崩 / for k in list(dd) 删干净
3. 报错名字就是检查项：名字里写 changed size，检查的是"元素个数"，那改 value 就不该犯规
4. 先确认类型再推结果：print(type(dd[k])) 看到 int，"加法会崩"这个判断当场推翻
```

**学到的规律**：

```
- 同一行错两次，说明"知道"和"手"是分开的两件事。E5 记了返回值 None，T2 手还是写成 print(sort())
- 索引越界会崩（IndexError），切片越界返回 []（不崩）—— 这两个必须分开记
- 想要它报错、又不想打断脚本 → try/except 包住，实验才能反复跑，还能每次复习
- 遍历时要用下标，必须让 i 是真下标（enumerate 不加 start）；
  只是想显示 1、2、3 的编号，才用 start=1
```

**面试能用**：

- "`sort()` 返回 None，如果写成 `print(lst.sort())` 排序会静默失效"——我一天内犯了两次，能讲清为什么会犯（知道 ≠ 手上形成习惯）
- "遍历字典时删元素会静默漏数据，所以先 `list(dd)` 固化再删"
- "遍历时改 value 安全、增删 key 抛 `RuntimeError`，因为迭代器怕漏读"
- "字典遍历默认给 key，不是 value，也不是序号"

**明天第一件事**：W1 Day5，把 T8 的 `todos` 写进 `todo.txt`，启动时读回来

---

## 2026-11-11（W1 Day5，跨到 11-12 04:35）

**做了什么**：`day5_practice.py` 跑完 A/B/T1-T7；主产出 `todo_v2.py` 做出持久化（存/读/加/删/标记全通）。`todo.txt` 从"不存在"到"3 条真实数据"，程序关掉再开数据还在。

**卡住的地方**：

```
1. T1 里 for i in s: i.strip() 完全没生效，输出的 '  数学' 还带着空格
2. B3 把 readlines() 写成 readline()，然后 for 遍历它，输出变成 '第' '一' '行' 一个字一个
3. T6 读完了但忘了 print，整段没有任何输出，我还在注释里写"不用 repr 也能看到 \n"
4. load_todos 里写成 row[1] == True，字符串比布尔永远 False，所有待办都被读成"未完成"
5. load_todos 写了、存盘存对了、文件内容也对，但程序行为是错的：
   顶上还写着 todos = [两条写死的]，从头到尾没调用过 load_todos()
6. "为什么要把 ['复习列表','0'] 变回 dict" 想了很久不懂
7. save_todos 该用 "w" 还是 "a"，我第一反应是 "a"
8. T7 追加 "赵六,88" 没加 \n，最后一行没有换行符
```

**怎么解的**：

```
1. 字符串不可变，i.strip() 返回新字符串，扔掉了就等于没做；
   而且 for x in 列表 里能改的只有"列表本身"，改不了 x。
   要么按下标 s[i] = s[i].strip()，要么推到新列表
2. readline 只读一行返回字符串，readlines 读全部返回列表。
   遍历字符串得到的是字符 —— for x in 什么决定 x 是什么
3. 先去看文件本身（字节级 reader），确认 '测试持久化,0' 真的存进去了，
   才发现问题不在存、在"根本没调 load_todos"
4. == 要和同类比：字符串跟 "1" 比，不是跟 True 比。而且这种错不报错，只出错
5. 写死的 todos 换成 todos = load_todos()，位置放在两个 def 之后（先定义后调用）
6. 因为主循环写的是 todo["title"]，只有 dict 能按名字取；
   列表只能 [0]。文件是存储格式，dict 是运行格式，中间必须转一次
7. save_todos 传进去的是整个列表，每次要"用内存覆盖文件"，
   用 "a" 会第 2 次保存就翻倍。"a" 只适合"只加一条，其余不动"
8. write() 不自动加换行，自己 + "\n"
```

**学到的规律**：

```
- 存/读要对称：存了没读 = 数据在文件里，但程序看不到。排查第一步永远是打开文件看，不是推逻辑
- 同一个函数里 def 和调用有先后：load_todos 必须在 todos = load_todos() 之前定义
- 字符串是只读的：所有方法返回新值，想改只能改容器或者重新赋值
- w 覆盖 / a 追加：判断标准是"我这次要保存整个状态，还是只加一条"
- 不报错的错最贵：== True、忘了调用、忘了 print，三个都不崩，但结果全错
- 我卡住的地方几乎全是"概念"而不是"语法"：
  变回 dict 的必要性、readline 单复数、w 和 a 的语义
```

**面试能用**：

- "我把 `save_todos` 用 `a` 模式写，测的时候发现第二次保存文件内容翻倍了。原因是 `a` 只能表达新增，表达不了修改和删除，而待办清单的核心操作恰恰是这两个。后来改成 `w` 覆盖整个文件，保证'文件 = 内存'"
- "有个 bug 我查了很久：数据明明存进文件了，但重新打开程序看不到。最后发现加载函数写了但从来没有被调用，程序用的还是写死在代码里的那份数据。从那以后我排查这类问题第一步是先打开文件确认内容，再查代码"
- "`line[1] == True` 这种写法不报错但结果永远错，因为从文件读出来的是字符串。测试里最怕这种静默失败"
- "字符串不可变，所以 `for x in lst: x.strip()` 是无效操作，必须改容器"

**今天没做完的（明天补，不跳过）**：

```
1. T4 结构不对：做成了 {名字: 字符串}，要求是 [{"name":..., "score": int}]
2. A4 / B6 的 except 里印的是手抄文本，不是真实异常（应 except X as e: print(type(e).__name__, e)）
3. T3 打印写死 "92 及格"，应该用变量
4. dict_drill.py 22 题没开始 —— 字典是后面所有内容的底座，必须先补
```

**明天第一件事**：`dict_drill.py` 的 A 区 8 题 + B 区 5 题（30 分钟），然后 W1 Day6 函数（Day7 的 `todo.py` 要把 save/load 抽成函数）

---

## 2026-11-12（W1 Day6）

**做了什么**：`dict_drill.py` 22 题全对；`day6_practice.py` 18 题全对（A 8 / B 5 / C 5）；`todo_v2.py` 抽出 `ask_index()`，标记完成和删除两处重复的 8 行消除，6 个输入回归全过

**卡住的地方**：

```
1. B5：把整个列表传给 get_score，报 TypeError: list indices must be integers
2. B5：函数体里还写了一行 sorted(...)，结果没人接
3. C2 find_best 逻辑全对但没 return，返回 None
4. D 区重构把 int(input(prompt)) 合到一行，结果 int() 跑到 try 外面，输入 abc 直接崩
5. ask_index 里 except 只 print 没 return，越界分支也没 return
6. A8 docstring 打印了整个，不是第一行
7. B2 用了 if lst == None 而不是 is None
```

**怎么解的**：

```
1. 分清分工：get_score(s) 只负责"给一个 dict 返回它的分数"，
   sorted(..., key=get_score) 负责"把每个 dict 依次交给它"。函数里不该出现 sorted
2. key=get_score 后面不能带括号 —— 带括号是"先算出一个值"，
   而且把列表当参数传进去，报的是同一个 TypeError
3. 加上 return ans。这是今天第 3 次"算了没交出去"（A6 故意、B5 静默、C2 忘 return）
4. int() 是可能失败的运算，必须放在 try 里。合并代码时把它挤出去了 ——
   这类"重构引入的回归"是最常见的真实事故
5. 每个异常分支都要 return None，否则函数继续往下走，而且后面会 NameError
6. area.__doc__.split("\n")[0]
7. 判断 None 一律用 is None（== 比的是值，is 比的是"是不是同一个对象"）
```

**学到的规律**：

```
- sorted 的 key= 要的是"函数本身"（不带括号），它会拿每个元素去调一次
- 函数的职责要单一：ask_index 只管拿到合法下标，不负责打印"已标记完成"、不负责存盘
- 函数里算出来的东西不 return 就是 None；表达式结果没被赋值/return/print 就是废的
- 重构时最容易丢的是"防御性代码"：try 的位置、异常的 return、边界检查
- 报错类型先看懂再改：list indices must be integers 说明传进去的是列表，不是字段名写错
```

**面试能用**：

- "我把两段重复的输入校验抽成 ask_index，重构之后输入 abc 反而崩了。原因是合并成 `int(input())` 时，我把转换动作挪到了 try 外面。这让我意识到重构最容易丢的就是防御性代码，所以改完必须把非法输入重跑一遍"
- "sorted 的 key 参数收的是一个函数，不是值。我一开始把整个列表传进去，报 list indices must be integers，才明白它是对每个元素各调一次"
- "写函数时如果算完没 return，调用方拿到 None 且不报错。我一天内犯了三次，现在写完会专门看一眼最后一行有没有 return"
- "函数的职责要单一：我的 ask_index 只负责拿到合法下标，不负责保存和提示成功，这样两个调用点都能复用它"

**明天第一件事**：W1 Day7 —— `todo.py` 成品（菜单收干净、改名）+ README + W1 周复盘 + 补累计小时

---

## 2026-11-13（W1 Day7）

**做了什么**：`todo_v2.py` 改名为 `todo.py`；菜单输出函数化（`print_menu` / `print_todos`）；新增 `show_stats` 进度统计；README 重写；修复调用时忘传 `todos` 参数的 bug

**卡住的地方**：

```
1. show_stats() 和 print_todos() 调用时忘了传 todos 参数，报 TypeError: missing 1 required positional argument
2. mark 写成 "[]" 而不是 "[ ]"，列表不对齐；而且 choice=="2" 分支里写的是对的，两处不一致
3. ask_index 里三处 return 没写 None（裸 return），虽然等价但意图不清
4. enumerate 又忘了用法，需要重新看演示才想起来
```

**怎么解的**：

```
1. 函数定义时有参数，调用时必须传。这是 Day6 刚学的，今天又犯了 —— 
   说明"知道"和"手上形成习惯"之间还有距离
2. 统一改成 "[ ]"，两处保持一致
3. 三处都改成 return None，显式表达"这里返回空值"
4. enumerate(列表, start=1) = 遍历时顺便报编号；for i, x in ... 拆开一对
```

**学到的规律**：

```
- 函数调用忘传参是最常见的低级错误，写完函数后立刻检查所有调用点
- 同一个逻辑在两处写时，必须保持一致（mark 格式、返回值写法）
- 显式 return None 比裸 return 好：意图清晰，且防止自己以后忘记加 return
- enumerate 两天不用就会忘，这是正常的；需要时回来查就行
```

**面试能用**：

- "我把 todo.py 的菜单输出抽成函数后，调用时忘了传 todos 参数，程序直接崩。这让我养成习惯：每次定义带参数的函数后，立刻搜索所有调用点确认参数齐全"
- "同一个 mark 格式在两个分支里写得不一样，一个 '[ ]' 一个 '[]'，导致列表不对齐。后来我统一用 print_todos 函数，只在一处定义格式"

---

## W1 周复盘（11/08 - 11/13）

**本周产出物**：python-basics 仓库，20+ commit，todo.py 可运行 ✅

**自评（1-5）**：4

**最大的问题**：

```
1. Day5 熬夜到凌晨 4:35，第二天效率明显下降。执行卡写了"不许熬夜补"，我没守住
2. 11/11 断了一天 commit（Day5 练习做了但没提交，直到 11/12 凌晨才 push）。
   "每天必须有 commit"这条规则破了一次
3. 同一个错误反复犯：return 忘写（Day6 三次）、int() 放错位置（Day6 重构时）、
   函数调用忘传参（Day7）。说明"知道"不等于"形成习惯"，需要更多刻意练习
```

**下周只改一件事**：**23:00 前必须停手**。Day5 那次熬夜是因为"想做完再睡"，但实际效果是第二天半天废掉。W2 开始严格执行：到点就停，没做完的进明天上午。

**基线对比**：

| T1 题目 | 11/08 答案 | 现在 |
|---|---|---|
| list 和 dict 的区别 | 不知道 | ✅ 能讲清：list 按位置取、dict 按名字取；dict 键唯一、可哈希；遍历默认给 key |
| 完整写出一段代码 | 只有 guess.py 18 行 | ✅ todo.py 112 行，含持久化、输入校验、函数化 |

**累计小时**：待补（11/08-11/13 六天，预估 35-40h，周日精确核算）

---

## 2026-11-13（W2 Day1）

**做了什么**：`day7_practice.py` 16 题全对（A6 + B5 + C5）；`day6_practice.py` 的 `format_params` 改成推导式版

**卡住的地方**：

```
1. C5 把 dict key 写成 "title:" 而不是 "title"，冒号跑进 key 里了
2. D 区 format_params 里用了全局变量 pairs_c 而不是参数 d
3. B3 一开始不知道元组列表怎么放进字典推导式
4. B4 不理解生成器和列表的区别
```

**怎么解的**：

```
1. dict 语法 {key: value} 里的冒号是分隔符，f-string 的花括号是插值。
   嵌套时先写 dict 结构再放 f-string：{"title": f"任务{i}"}
2. 函数体里只能用参数/局部变量/内置函数，看到外部全局变量就要警觉。
   这和 Day6 C2 用 max 覆盖内置函数是同一种"作用域混淆"
3. for name, score in students_b 在推导式里和普通 for 循环里完全一样，
   元组自动解包成两个变量
4. [...] 方括号立刻算完占内存；(...) 圆括号是待计算公式，sum/list/for 触发计算，
   且只能用一次
```

**学到的规律**：

```
- 推导式里 if 在 for 后是过滤，if-else 在 for 前是映射，位置不同含义完全不同
- 生成器省内存但只能用一次，大数据量+单次遍历时用
- *args 解包成位置参数，**kwargs 解包成关键字参数，W2 Day6 requests 会用到
- 不是所有代码都适合改成推导式：计数模式、双目标分组用传统 for 更清晰
```

**面试能用**：

- "列表推导式里 if 放 for 后面是过滤，放前面是三元映射。我一开始混过，后来记住'过滤在后、映射在前'"
- "生成器表达式用圆括号，惰性求值省内存，但只能消费一次。读大文件逐行处理时用生成器不会爆内存"
- "函数体里误用了外部全局变量而不是参数，测试碰巧能过但换输入就错。现在写完函数会检查一遍变量来源"

**明天第一件事**：W2 Day2，类与对象（__init__ / 实例方法 / 继承）

---

## 2026-11-14（W2 Day2，从 11-13 23:00 开始）

**做了什么**：`day8_practice.py` A 区 5 题 + B 区 4 题 + C 区 5 题全对；**把 `todo.py` 整个从 dict 改成 `Todo` 类**（`to_line` / `from_line` 双向转换 + `mark_done` 方法），全功能回归通过

**卡住的地方（按提问顺序）**：

```
1. B4 的 isinstance 看不懂："再用 isinstance 判断普通 Todo" 这句在问什么？
2. 每个类方法都必须有 self 参数吗？
3. C3 卡住：sorted 写完 print 还是原顺序，而且打印出一堆内存地址
4. C4 不知道怎么"抛出"异常：try/except 写了，但余额不足时什么都没发生
5. cls 是什么？和 self 有什么区别？
6. line.strip().split(",") 返回的到底是什么？
7. 为什么不是返回整个文本的列表？
8. A6 和 B5 我明明写了，为什么控制台没输出？
9. 为什么 hello() 要有 self 参数？
10. 可是 hello() 里面也没有实例属性啊？
11. 为什么 print(f"{i}. {todo}") 可以直接靠 __str__？
12. i 和 todo 这两个参数是怎么传进 __str__ 的？
13. todo 是 Todo 的实例吗？在哪里声明的？
14. 我还是有点懵（对象/变量/方法之间的关联）
```

**怎么解的**：

```
1. isinstance 是"能不能当这个类用"（会往上找父类），type() is 是"精确是哪个类"。
   三个对比：isinstance(子, 父)=True / isinstance(父, 子)=False / type(子) is 父=False
2. 普通方法必须有；@staticmethod 不要；@classmethod 用 cls。
   根因不是"方法需要数据"，而是"通过实例调用时会多传一个参数，必须有位置接住"
3. sorted() 返回新列表，不接住就白算（第 4 次踩"算了没交出来"）。
   而且 print(列表) 用的是元素的 __repr__，不是 __str__，所以要么循环逐个 print，要么加 __repr__
4. 抛异常用 raise ValueError("余额不足")。try/except 只能"接住"，不会"制造"异常
5. cls 是类本身（<class 'Todo'>），self 是实例（<Todo object at 0x...>）。
   cls(...) 就是"用这个类造实例"，子类调用时 cls 是子类，所以 from_line 对子类也正确
6. 返回 ['买牛奶', '0'] —— 一个列表，元素全是字符串。
   所以 row[1] == "1" 而不是 == 1；len(row) < 2 是防"没有逗号"和"空行"
7. split 的语义就是"按分隔符切开、扔掉分隔符"。整行要靠 readlines 那层给。
   两层各管一层：readlines 切行，split 切字段
8. A6 调的是 Guyi.hello()（类调用，不绑实例，不报错），要 Guyi().hello()；
   B5 没报错是因为 Todo 里有 title = "" 这个类属性兜底，把真正的 bug 掩盖了
9. 因为 t.show() 实际等价于 Todo.show(t)，Python 自动把实例塞成第一个参数
10. Python 不看函数体用不用 self，它只按协议绑定。不用实例数据就该写 @staticmethod
11. f-string / str() / print(单个对象) 都走 __str__；print(列表/字典) 走元素的 __repr__
12. i 和 todo 根本没进 __str__ —— __str__ 只收 self。
    f-string 是在外面把 {i} 和 {todo} 分别转成字符串再拼接，print 只收到拼好的那一个字符串
13. todo 是 for 循环变量，不是单独声明：for i, todo in enumerate(todos, ...) 这一行就是声明处，
    每圈重新绑定；todo is todos[i-1] 为 True，说明是同一个对象，不是副本
14. 根因是从"字典"跨到"类"这道坎。用 8 行最小例子（造两个实例 → 装列表 → 贴标签 → f"{todo}"）
    才看清：类是模板、实例是造出来的东西、变量名只是标签
```

**学到的规律**：

```
- self 不是"要用实例数据"的标记，是"实例调用必传第一个参数"的协议结果
- 方法内部看 self，方法外部看类型；obj.method() 等价于 Class.method(obj)
- __str__ 只管"我长什么样"，编号这种显示层信息在外层拼，不该进对象
- print(容器) 走 repr，print(元素) 走 str；对象放列表里想好看就得加 __repr__
- raise 是"报警"，try/except 是"接警"，两者分工不能混
- 类属性会被实例属性"继承兜底"，所以数据类不要给属性占位（title = "" 会掩盖漏初始化）
- 对象不知道自己在列表里第几个，这是显示层的事
```

**面试能用**：

- "我从字典存数据改成类，是因为加字段时容易写错 key 还不报错。改成类后，字段名写错在 `__init__` 就暴露了，而且'标记完成'变成了对象自己的方法"
- "`obj.method()` 等价于 `Class.method(obj)`，所以方法必须有 self 接住——不是语法规定，是绑定机制决定的"
- "print(列表) 打印的是元素的 repr，不是 str。我在做成绩排序输出时踩过，列表里全是内存地址"
- "抛出和捕获是两件事：`raise` 主动报错让上层决定怎么办，`try/except` 负责接住。只写 try/except 不会产生异常"

**今天没做完 / 明天补**：

```
1. A6 / B5 两个错误实验没真正触发（A6 少了实例括号，B5 被类属性兜底）
2. A1 里的 title = "" / done = None 两行类属性该删（会掩盖 bug）
3. day8 的 C3 用了 print(r, end=" / ") 会多打一个尾部分隔符
```

**明天第一件事**：开始前先用一个完整小例子把"实例 / 变量 / 方法 / __str__ 的关联"串一遍（今天懵在这里，不留坑），然后进 W2 Day3 异常处理

---

## 2026-11-14（W2 Day3 · 异常处理）

**做了什么**：`day9_practice.py` 21 题全对（A 区 try/except/else/finally 完整形态、B 区 5 个异常类型、C 区 raise/裸重抛/异常链、D 区 TodoError 自定义异常家族 + add_todo/get_todo）；跟敲廖雪峰「错误处理」节（`lxf.py`）

**卡住的地方**：

```
1. A2 的 else 永远不执行：return a/b 写在 try 里，函数当场结束，else 没机会跑
2. add_todo 里写了 if title.strip() == " "，条件永远为 False，
   全空格标题静默混进列表，异常永远抛不出来
3. B 区先预测再跑：5 个只对了 1 个。
   "2"+2 猜成 ValueError（实际 TypeError）、None.title 猜成"ClassError"（实际 AttributeError，根本没有这个异常）
4. D4 设计题"同样是编号越界，ask_index 为什么 return None、get_todo 为什么 raise"，第一反应是不知道
```

**怎么解的**：

```
1. else 的执行条件 = try 完整跑完且没被 return/break 提前退出。
   修法：try 里只计算存变量，else 做成功后的动作，return 放最后统一出口。
   对照记：finally 连 return 都拦不住（A6 实测），else 会被 return 跳过
2. strip() 的产物两端不可能有空格，跟 " " 比较是自己和自己的定义打架。
   判空的通用模式：if not title.strip()
3. 口诀：TypeError=类型不对；ValueError=类型对、值不行；AttributeError=对象没有这个属性/方法。
   AttributeError 有真实案例：前天 dict 没改成 Todo 时报的
   'dict' object has no attribute 'to_line' 就是它
4. 答案：错误由谁处理，决定错误怎么传。
   ask_index 调用方只有菜单、处理方式已知且固定（提示+continue）→ 就地消化 return None；
   get_todo 是通用函数、无法预知调用方想怎么办 → raise 抛出去，把处理权交给调用方
```

**学到的规律**：

```
- try → 成功走 else / 失败走 except → finally 无论如何最后走；finally 在 return 之后仍执行
- raise 三形态：抛新的 / except 里裸 raise 原样重抛 / raise X from e 记因果链（e.__cause__）
- 自定义异常要建家族基类（TodoError），调用方 except TodoError 一网打尽，不误接别的库的错
- except 范围越窄越好：能用 TodoError 就不用 Exception，裸 except: 从今天的起禁用（会吞 Ctrl+C）
- 数据进门先清洗：add_todo 存 title.strip() 而不是原始输入，脏空格就不会一路跟到 todo.txt
- 静默失败比崩溃危险：永假条件不报错、数据悄悄变脏，这是"不报错的错最贵"的又一案例
```

**面试能用**：

- "异常处理不是'别让程序崩'，是'崩溃的边界要可控'。预期内、调用方能处理的错用 return None 就地消化；不该发生、处理方式未知的错用 raise 抛出去让调用方决定"
- "我写校验时用过 `title.strip() == " "` 这种永假条件，程序不报错但脏数据进了列表。从此判空一律 `not x.strip()`，并且校验函数必须配'非法输入'测试用例"
- "自定义异常建家族基类，调用方一个 except 接住整个模块的错误，异常名字本身就是文档"
- "finally 和 else 的区别：return 之后 finally 仍执行、else 被跳过——所以清理资源放 finally（或直接用 with）"

**明天第一件事**：W2 Day4，模块与包（import / `__name__ == "__main__"` / pip）—— 把 day9 里的 TodoError 家族抽成独立模块 `todo_errors.py`，正好用上 import

---

## 2026-11-16（W2 Day4 · 模块与包）

> 11/15 休息日（主动申报，计划内恢复）。

**做了什么**：`day10_practice.py` 17 题全对（A 区 import 四形态 + sys.path + 缓存、B 区 `__name__` 两态、C 区自建 `myutils.py`、D 区 json 对比手写 CSV）；新建 `mytool.py` / `myutils.py`；**主产出：`todo.py` 拆三件套**（`todo_errors.py` 异常家族 / `todo_core.py` 数据层 / `todo.py` 界面层），全功能回归 12 步通过，`todo.txt` 基线还原

**卡住的地方**：

```
1. 添加事项后保存时崩：AttributeError: 'str' object has no attribute 'to_line'。
   根源在 todo_core.py 的 add_todo：todos.append(title) 塞的是裸字符串，
   而列表里装的应该是 Todo 对象——day9 的 D 区是字符串列表，搬运时数据类型没跟着升级
   （和 W2 Day2 的 L86 append dict 忘改是同一类"重构漏改写入点"）
2. todo_errors.py 搬运时把 get_todo/add_todo 缩进进了异常类的类体里，
   变成了 InvalidIndexError/EmptyTitleError 的"方法"，其中 add_todo 还是带 bug 的旧版。
   不崩（没人调用），是死代码
3. A6 验证缓存写了 id(math) is id(math)，输出 False
4. A1 忘做"保留 2 位"，输出了 3.141592653589793
5. 0 区自测：Q1 只答了概念没答调用写法区别；Q5 写 pip install 而不是 python -m pip install
```

**怎么解的**：

```
1. 排查路径：崩在 save_todos（出口），但坏数据是 add_todo（门口）放进去的。
   修：todos.append(Todo(title.strip()))——包一层 Todo + 进门清洗。
   附带发现：save 用 "w" 先清空再写，写到第 4 条才崩，前 3 条恰好=原内容所以文件"侥幸"没坏
   （部分写入风险的真实案例）
2. 缩进层级决定名字归属：同一个 def 在模块顶层是函数、缩进进类体就是方法。
   修法：删掉两段死代码，todo_errors.py 只留 3 个类定义
3. is 比较对象身份、== 比较值。id() 每次返回新建的大整数对象（>256 不缓存），
   两次调用值相等但身份不等 → is False。改 math is math → True
   （实测：id==id True / id is id False；缓存最直观证据是 mytool 顶层行只打印一次）
4. f"{math.pi:.2f}"
5. Q1 补：import math 后调用要 math.sqrt(144)；from math import sqrt 后直接 sqrt(144)。
   Q5 补：机器上有 3.10 和 3.11 两个 Python，裸 pip 装进哪个看运气，必须 python -m pip
```

**学到的规律**：

```
- import 顶层代码只在首次导入时执行，之后走 sys.modules 缓存；sys.path[0] = 脚本所在目录
- __name__ 两态：直接跑 = "__main__"（守卫内执行），被 import = 模块名（守卫内跳过）。
  一个文件既能当库又能当脚本，靠的就是这个守卫；todo_core 被 import 时绝不能自己跑起来
- 三件套依赖必须单向：todo.py → todo_core.py → todo_errors.py
- 循环导入实测（AI 代跑，两个入口行为不同）：python todo.py 入口崩
  ImportError: cannot import name 'Todo' from partially initialized module；
  python todo_core.py 入口不崩——但入口文件叫 __main__，todo.py 的 import 会把
  todo_core 重新加载第二份，内存里出现两份 Todo 类，跨份 isinstance 全 False。
  结论：循环导入最坏的情况不是报错，而是不报错
- 手写 CSV 的死角：标题含逗号 → '买牛奶,面包,0' split 读回 ['买牛奶','面包','0']，数据损坏；
  json.dumps(ensure_ascii=False) 往返一致 True。真实项目用 JSON 的原因亲眼见到了
- 包 = 带 __init__.py 的目录；from mypkg.validators import not_empty 可用
- 搬代码三查：查写入点数据类型（append 的是什么）、查缩进层级（进没进类体）、查守卫（会不会自己跑）
```

**面试能用**：

- "`if __name__ == '__main__'` 的作用：让模块既能被 import 复用、又能直接运行自检。被导入时 `__name__` 是模块名，守卫内代码不执行"
- "我做过多文件拆分：界面层/数据层/异常层单向依赖。反向 import 会循环导入，我实测过它有两种表现——正门报 partially initialized ImportError，另一个入口不报错但模块被加载两份、isinstance 失灵，所以依赖单向是唯一保险"
- "手写 CSV 遇到字段内含分隔符就损坏，json 序列化往返一致。我的 todo 项目后来理解了为什么工业界用 JSON"
- "AttributeError 排查经验：报错位置不一定是错误位置。我的 save 崩在 str 没有 to_line，真正原因是 add 时 append 了裸字符串——从写入点查起，不是从崩溃点改起"

**明天第一件事**：W2 Day5，venv 虚拟环境 + requirements.txt（把三件套的依赖管理正规化，为 Day6 requests 做准备）

---

## 2026-11-16（W2 Day5 · venv 与 requirements.txt）

**做了什么**：给 `python-basics` 建了 venv（**2299 个文件 / 32.1 MB**，装完包后），装 `requests 2.34.2` + `pyfiglet 1.0.4`；导出 `requirements.txt`（6 条，UTF-8 无 BOM）；`.gitignore` 加 `venv/` `.venv/`，`git status --untracked-files=all` 从 **779 行降到 5 行**；`day11_practice.py` 17 题里 14 题跑通（A 区 3 道 shell 题留空）；`todo.py` 在 venv 里回归通过（3 条待办原样）；README 补「怎么跑」四行

**卡住的地方**：

```
1. pip install requests 卡 40-60 秒，输出停在 Looking in indexes: 之后一个字不动。
   关掉重来还是卡，换清华镜像源也卡，加 --timeout 也没用（不是超时，是没超时）
2. VS Code 的 PS 里 .\venv\Scripts\Activate.ps1 报：
   "无法加载文件 ...\Activate.ps1，因为在此系统上禁止运行脚本"
   （Get-ExecutionPolicy 全部是 Undefined）
3. pip freeze > requirements.txt 之后文件是 UTF-16LE（od -c 首字节 377 376），
   字符之间夹 \0。诡异的是 pip install -r 能正常读（靠 BOM 识别），
   所以不会立刻报错——最阴的一种
4. 在 C:\WINDOWS\system32 目录下跑 python -m venv venv → WinError 5 拒绝访问；
   在项目目录重跑 → Error: [Errno 13] Permission denied: '...\venv\Scripts\python.exe'
5. PowerShell 里 where python 一行输出都没有
```

**怎么解的**：

```
1. 先用 --no-cache-dir 对照：3.3 秒装完 → 说明网络没问题，问题在缓存。
   再用 faulthandler 抓栈（python -X 跑 pip._internal.cli.main.main，
   dump_traceback_later(6, repeat=True)），栈顶原文：
     tempfile.py:253 in _mkstemp_inner      ← name = next(names)
     tempfile.py:577 in opener / 580 NamedTemporaryFile
     pip/_internal/utils/filesystem.py:53 adjacent_tmp_file
     pip/_internal/network/cache.py:77 _write / 86 set
   → 响应已经收完，卡在"把 body 写进 HTTP 缓存、创建临时文件"那一步。
   机制：tempfile._mkstemp_inner 在 for seq in range(TMP_MAX) 里循环 os.open，
         只捕 FileExistsError 和特定 PermissionError；Windows TMP_MAX=32767，
         缓存目录里有 delete-pending 的坏文件 → 一直 ACCESS_DENIED → 空转几万次 = 几十秒静默。
   pip cache purge 印证：wheels/0f/0e/7a/3094a4ce.../docx2txt-0.8-...whl
   PermissionError: [WinError 5] 拒绝访问（ACL 正常，是句柄占用）
   解法：rm -rf AppData/Local/pip/Cache（677 MB / 3055 文件）→ 40s 降到 2.4~3.2s
   排除过：网络 0.29s/200、目录本身 os.open 100 次 0.038s 全成功、
          Defender 实时保护关闭、ACL 完全控制、两个僵尸 pip 进程（杀了还卡）
2. .\venv\Scripts\Activate.ps1 被执行策略挡。解法：Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   或干脆用 cmd 的 venv\Scripts\activate.bat，或用 Git Bash 的 source venv/Scripts/activate
3. PowerShell 5.1 的 > 重定向默认写 UTF-16LE。解法：python -m pip freeze | Set-Content requirements.txt -Encoding ascii
   （或 cmd 里 type、或 python 自己 open(..., "w", encoding="utf-8") 写）
   验证：(Get-Content requirements.txt).Count = 6，Format-Hex 首字节不是 FF FE
4. 两个独立问题：WinError 5 是没 cd 到项目目录（venv 是相对路径）；
   Permission denied 是 VS Code 的 black-formatter 扩展正拿着 venv\Scripts\python.exe 在跑，
   Windows 不允许覆盖运行中的 exe。解法：cd 到项目目录 + 关掉 VS Code / 换名 python -m venv venv2 / --clear
5. where 在 PowerShell 里是 Where-Object 的别名，对空管道静默。解法：where.exe python
   （同类坑：curl → curl.exe、wget → wget.exe、sc → sc.exe）
```

**学到的规律**：

```
- venv 是「文件的身份」，不是「进程的状态」。激活只做一件事：把 venv\Scripts 插到 PATH 最前，
  让你敲 python 时命中的是 venv 的 exe。直接写 venv\Scripts\python.exe 跑，等于跳过 PATH 查找，
  没激活也照样在 venv 里——判定依据永远是 sys.executable / sys.prefix，不是提示符
- venv 里的 python.exe 是「启动器」不是复制品：它启动时往上翻两层找 pyvenv.cfg，
  读 home 和 include-system-site-packages，据此设 sys.prefix / sys.base_prefix。
  把 pyvenv.cfg 改名，同一个 exe 立刻"变回"全局环境——1 KB 的配置决定 2299 个文件算不算一个环境
- 隔离是双向的：venv 装的 pyfiglet 全局看不见（ModuleNotFoundError），全局的 requests 在
  venv 里也看不见（除非 include-system-site-packages = true）。venv 自带的只有 pip + setuptools
- pip freeze 和 pip list --format=freeze 不一样：freeze 默认不列 pip/setuptools（避免把它们写进依赖清单）
- 「网络很快但命令卡住」的排查顺序：先 --no-cache-dir 对照 → 二分出是网络还是本地 →
  再用 faulthandler 抓栈看卡在哪个函数。抓栈比猜快一百倍
- 静默卡顿的共同特征：底层在 range(N) 里重试且只捕获了部分异常。TMP_MAX=32767 就是这么来的
- PowerShell 5.1 的 > 和 Add-Content 默认不是 UTF-8（> 是 UTF-16LE，Add-Content 是 GBK），
  写任何要被别的工具读的文件都不能用它。中文注释尤其危险
- .gitignore 要在建环境之前写。漏了的话 venv 会以 779 个未跟踪文件的形式出现在 git status 里，
  一旦 git add . 就进了仓库（26 MB，且换机器后路径全是错的）
- 需要重建 venv 的三种场景：换 Python 版本（只能重建，不能改）、加了 --system-site-packages、
  环境装乱了。重建前先 --clear 或删目录，但必须没有任何进程占着里面的 exe
```

**面试能用**：

- "虚拟环境解决的问题：一台机器上有多个项目，A 要 requests 2.28、B 要 2.34，装在全局就冲突。venv 给每个项目一个独立的 site-packages，靠 `pyvenv.cfg` 让 python.exe 认自己的 prefix。判断当前在哪个环境看 `sys.prefix` 和 `sys.base_prefix` 是否相等"
- "激活的本质是改 PATH 的查找顺序，不是切换进程状态。所以 `venv\Scripts\python.exe xxx.py` 和激活后 `python xxx.py` 效果一样。我踩过没激活就 pip install 的坑——包直接进了全局，这种错误不会报错，只能靠装包前 `where pip` 防"
- "requirements.txt 是依赖清单不是环境快照。`pip freeze` 只列第三方包不列 pip 本身，`pip install -r` 是幂等的（已满足就打 already satisfied）。生产上还要锁版本和 hash，我理解原理后自己写的 freeze 清单"
- "排查过一个 pip 卡 40 秒的问题：网络 0.3 秒就通，但 install 静默卡住。用 faulthandler 抓栈发现卡在 tempfile 创建临时文件，根因是 pip 的 HTTP 缓存目录里有句柄未释放的坏文件，Windows 上 tempfile 会重试 32767 次才放弃。删缓存目录后恢复到 3 秒。这个排查思路是「先二分现象（--no-cache-dir），再抓运行时栈，别猜」"

**明天第一件事**：W2 Day6，requests 库（GET/POST、headers、params、json、超时、状态码）——现在有了 venv，装第三方包不会再污染全局

---

## 2026-11-17（W2 Day6 · requests GET + 安全请求）

**做了什么**：`day12_practice.py` 13 题全跑通（A 区 Response 解剖 4 题、B 区状态码与安全请求 3 题、C 区 params/headers 3 题、D 区 timeout 3 题）；主产出 `get_ip.py`（查公网 IP，四种失败模式都给人话提示）；讲义从旧版 1072 行重写到 518 行，砍掉 POST/Session/cookies/stream，只保留 GET + 响应读取 + 安全请求

**卡住的地方**：

```
1. get_ip.py 第一次跑报 KeyError: 'oringin'
   → 拼写错误，origin 写成了 oringin。改了就好
2. 验收第 4 条把 timeout 改成 0.001 测超时提示，测完忘改回 10
   → 之后每次跑都报"请求超时"，以为网络坏了，其实是自己埋的雷
3. 跑完 13 题后说"我还不知道 requests 是什么"
   → 会用但没从高处看过。它就是一个帮你发 HTTP 请求的函数库，
     等价于浏览器地址栏输入 URL 按回车，区别是把响应变成 Python 对象让你用代码处理
```

**怎么解的**：

```
1. KeyError 报错信息里直接写了缺失的键名 'oringin'，对照 httpbin 文档发现是 origin
2. 验收测试改参数后要立刻改回来，或者用单独的测试脚本而不是改主文件
3. requests = urllib 的好用封装。标准库 urllib 能发请求但难用，requests 三行变一行。
   今天只是学会"怎么用锤子钉钉子"，W4 会教"钉子是什么、为什么要钉"，W5 才是真正战场
```

**学到的规律**：

```
- requests.get() 返回 Response 对象，不是字典。r.json() 才返回字典
- 404/500 不抛异常——requests 只对通信失败（连不上/超时）抛异常，HTTP 业务失败当正常响应。
  不看状态码就 r.json() → JSONDecodeError，报错信息完全看不出是 404 导致的
- raise_for_status() 把 4xx/5xx 变成 HTTPError，消息里带状态码和 URL，比 JSONDecodeError 有用一百倍
- r.text 是解码后的 str，r.content 是原始 bytes。改 r.encoding 后重读 r.text 会变
- 中文乱码不是服务器坏了，是解码方式不对。Content-Type 没写 charset 时 requests 按规范猜 ISO-8859-1，
  UTF-8 中文被当成拉丁字符 → 乱码。修正：r.encoding = r.apparent_encoding
- timeout=5 不等于"总共 5 秒"，是"连接最多 5 秒 + 每次读最多 5 秒"。不写 timeout = 无限等
- ReadTimeout 和 ConnectionError 是两种不同的失败：前者连上了但等内容超时，后者根本没连上
- safe_get 模板：try → get → raise_for_status → return，except 分别捕 Timeout/ConnectionError/HTTPError，
  每个 except 给人话提示而不是 Python 栈
```

**面试能用**：

- "requests 如何处理 HTTP 错误状态码？不自动抛异常，r.ok 是 status_code<400，要主动 raise_for_status() 才抛 HTTPError"
- "timeout 参数限制什么？连接超时和读超时的上限，不是总时长；不写就是无限等"
- "r.text 和 r.content 区别？content 是 bytes 原始，text 是按 encoding 解码的 str；改 encoding 后重读 text 会变"
- "怎么处理中文乱码？先看 Content-Type 的 charset；没有就 r.encoding = r.apparent_encoding；改完要重读 r.text"

**明天第一件事**：W2 Day7 综合实战——写 weather_cli.py，调 wttr.in API 查天气。今天学的 GET + json() + 异常处理 + timeout 全用上

---

## 2026-11-17（W2 Day7 · 天气查询脚本）

**做了什么**：`weather_cli.py` 99 行，调 wttr.in API，输入城市名输出当前天气 + 未来 3 天预报；六条验收全过（Beijing/Chengdu 正常输出、无参数给用法提示、不存在城市给友好错误、断网重跑成功、todo.py 回归通过）；讲义 453 行

**卡住的地方**：

```
1. wttr.in 不稳定，第一次跑报"连不上"，重跑就通了
   → 不是代码问题，是该站偶尔抖动。Day6 学的异常处理正好兜住了：
     给人话提示、不崩、能重试
2. wttr.in 的坑（讲义里提前写了，但亲手撞一遍才记住）：
   - 所有数值都是字符串（"7" 不是 7），显示时直接用，计算时要 int()
   - 不存在的城市返回 500 + 纯文本，不是 404 + JSON
     → 不能直接 r.json()，要先查 status_code
   - 中文城市名能用但识别不准（"成都"→"Pihsien"即郫县）
3. 错误分层的体会：get_weather 抛 RuntimeError，main 只捕 RuntimeError 翻译成人话
   → 底层细节（Timeout/ConnectionError/HTTPError）不泄漏到入口层
```

**怎么解的**：

```
1. wttr.in 抖动靠重试解决，不需要改代码。如果频繁遇到可以加自动重试（2 次 + sleep 2s）
2. 先查 r.status_code != 200 再决定读 r.text 还是 r.json()
3. 函数职责分离：get_weather 只管"取数据+格式化"，main 只管"解析参数+打印+退出码"
   → 以后写测试可以直接调 get_weather("Beijing")，不用模拟命令行
```

**学到的规律**：

```
- sys.argv[0] 是脚本名，sys.argv[1] 才是第一个参数；len(sys.argv) < 2 = 没传参
- sys.exit(1) = 出错退出，shell/CI 靠这个判断成功失败
- if __name__ == "__main__" 让文件既能当脚本又能被 import（Day4 学过，今天第一次用在真实项目里）
- 公开 API 不一定稳定，timeout 和重试是必须的
- 第一个"能给别人演示"的程序 = W2 前六天知识的串联：venv + requests + 异常处理 + 命令行参数
```

**面试能用**：

- "我独立用 requests 写了一个命令行天气查询工具，调 wttr.in 公开 API，支持任意城市查询当前天气和未来 3 天预报。做了完整的异常处理：超时、断网、城市不存在、数据格式异常都有友好提示，不会给用户看 Python 栈。代码结构上把 API 调用和命令行入口分开，方便以后加测试"

**W2 周复盘预告**：W2 技术内容全部完成。下一步做周复盘（自评 + commit 统计 + W3 准备）

---

## W2 周复盘（11/14 - 11/17）

**本周产出物**：weather_cli.py（调 wttr.in API 查天气，99 行，四种失败给人话提示）+ get_ip.py + todo.py 三件套 + venv 环境 + requirements.txt ✅

**自评（1-5）**：4

**最大的收获**：

```
1. 从"会写 Python"跨到了"能从网上取数据"。Day6 之前所有操作都是本地的，
   Day6-7 第一次跟外部世界打交道。这个跨越比 W1 任何一天都大
2. 异常处理从"语法"变成了"工程"。Day3 学了 try/except 的写法，
   Day6-7 才真正体会到为什么要分层：底层抛 RuntimeError，顶层翻译成人话。
   用户不该看到 Traceback，该看到"连不上 wttr.in，检查网络连接"
3. 讲义重写的体会：Day6 第一版写了 1072 行，自己回头看发现看不懂。
   砍到 518 行、只保留 GET + 响应 + 安全请求后，反而学得更扎实。
   贪多嚼不烂是真实教训
```

**最大的问题**：

```
1. Day1-Day3 在 W1 末尾提前完成了（11/13-11/14），导致 W2 实际只用了 4 天（11/14-11/17）。
   节奏偏快，Day6 讲义写过头就是后果之一
2. Day6 讲义第一版 1072 行，远超前几天 300-500 行的节奏。
   说明我在"控制粒度"这件事上还没形成直觉，需要刻意约束
3. weather_cli.py 是我写的不是你自己写的。虽然你跑通了验收，
   但"复制粘贴能跑"和"自己从零搭出来"差距很大。
   Day7 的练习应该自己重写一遍，不能只靠我的版本过关
```

**下周只改一件事**：**讲义写完先自己读一遍，超过 500 行就砍**。Day6 的教训不能再犯。另外 Day7 的 weather_cli.py 要自己从头写一遍，不看我的版本。

**基线对比**：

| T1 题目 | 11/08 答案 | W1 结束 | W2 结束 |
|---|---|---|---|
| list 和 dict 的区别 | 不知道 | ✅ 能讲清 | ✅ 同左 |
| 完整写出一段代码 | guess.py 18 行 | todo.py 112 行 | weather_cli.py 99 行 + get_ip.py + todo 三件套 |
| Java 定义一个类的语法 | 忘了 | — | W2 Day2 学了 Python 类，Java 语法仍不会（不在计划内） |
| C 语言指针 | "变量的存储位置" | — | 未复测（不在计划内） |
| 梯度下降 | "减少误差？" | — | 未复测（不在计划内） |

**commit 统计**：

| 指标 | W1 结束 | W2 结束 | 增量 |
|---|---|---|---|
| 总 commit 数 | 27 | 31 | +4 |
| W2 新增文件 | — | 14 个 | mytool/myutils/todo_core/todo_errors/day10-12_practice/get_ip/weather_cli/requirements/.gitignore 等 |

**累计小时**：待补（11/14-11/17 四天，预估 20-25h）

**W3 预告**：测试理论 + 用例设计。从"会写代码的人"变成"懂测试的人"。这是测试岗面试的第一道门槛，也是回报率最高的一周（面试必考，且唯一能靠背诵+练习拿满分的部分）。

---

## 2026-11-18（W3 Day1 · 测试定义与七大原则）

**做了什么**：学习软件测试定义、目的、七大原则、测试与调试的区别；配套题库 Q1-Q2；默写七大原则 + 用自己的话举例 + 录音自检

**卡住的地方**：

```
1. 自测 5 题中"穷尽测试不可能→那怎么办"一开始答不上来
   → 讲义里给了答案：等价类划分 + 边界值分析 + 风险驱动。
     这就是测试方法论存在的意义——不是穷举，是聪明地选
2. 七大原则第 6 条"依赖背景"和第 7 条"无缺陷谬误"容易混
   → 区分：第 6 条说"不同项目策略不同"，第 7 条说"没 bug ≠ 可用"
3. 录音第一遍打了两次磕巴：杀虫剂悖论的例子没想好
   → 用 todo.py 的例子重录："第一次测出 off-by-one，后来同样的输入再也找不到新 bug"
     第二遍流畅通过
```

**学到的规律**：

```
- 测试只能证明有缺陷，不能证明没有缺陷（Dijkstra）——这是行业基石
- 测试 vs 调试四字区分：找人修 vs 自己修
- 口诀"显穷早集杀背谬"比逐条背快十倍
- "看懂了"≠"能说出来"，录音是唯一检验标准
```

**明天第一件事**：W3 Day2 测试分类（四层级/三方法/四维度）

---

## 2026-11-19（W3 Day2 · 测试分类）

**做了什么**：学习按阶段分（单元/集成/系统/验收）、按方法分（黑盒/白盒/灰盒）、按内容分（功能/性能/安全/兼容）；配套题库 Q8；画两张表 + todo.py 分类练习 + 录音 2 分钟

**卡住的地方**：

```
1. 练习 2"给 todo.py 列 8 条测试分类"一开始列不出来
   → 不是不会分类，是没把 todo.py 的功能拆成可测试的点。
     跟着示范思路（每个菜单操作 × 每个维度 = 一条）后自己列出 6 条：
     - 标记99越界不崩 / 标记字符串不崩 / 删除字符串不崩（系统/黑盒/功能）
     - ask_index 传入空字符不崩（系统/白盒/功能）← 知道函数名所以标白盒
     - 安卓苹果运行不报错（系统/黑盒/兼容）
     - 连续添加1000条耗时<2s（系统/黑盒/性能）
2. 集成测试和系统测试的区别一开始说不清
   → 集成测"连接处"（模块间接口），系统测"全流程"（用户视角端到端）
```

**学到的规律**：

```
- 四层级从小到大：单→集→系→验，谐音"单机系验"
- 黑盒=用户视角不看代码，白盒=开发视角看覆盖率，灰盒=半透视（接口测试）
- 四种内容维度一句话：功能=对不对、性能=快不快、安全=漏不漏、兼容=通不通
- W2 做的 weather_cli.py 验收六条全是功能测试，其他三个维度还没碰
- 同一个测试点可以标不同方法：知道代码标白盒，不知道标黑盒，都对
```

**面试能用**：

- "测试按阶段分单元/集成/系统/验收四层，粒度从小到大；按方法分黑盒/白盒/灰盒；实际工作中我做得最多的是系统级黑盒功能测试，也接触过接口层面的灰盒测试"

**明天第一件事**：W3 Day3 黑盒方法 1——等价类划分 + 边界值分析。Day7 的 60 条登录用例全靠这两个方法

---

## 2026-11-20（W3 Day3 · 等价类划分 + 边界值分析）

**做了什么**：学习等价类划分（有效/无效）和边界值分析（±1）；给 todo.py 标题字段设计 10 条测试数据；练习密码字段 13 条、年龄字段 10 条；录音自检

**卡住的地方**：

```
1. 练习 1 密码字段第一版把边界值全标成了 E（有效类）
   → 边界(a-1) 和边界(b+1) 是无效的，不应标 E。
     边界值和等价类是两个维度，标注时要分开：
     a-1/b+1 标 I/边界，a/a+1/b-1/b 标 边界
2. 练习 1 漏了纯字母和纯数字两个有效等价类
   → 规格允许字母/数字/下划线三种字符类型，每种至少一个代表值
3. 练习 2 的 I1(18.5) 和 I3(0.01) 都是"非整数"，有重叠
   → 实际测试中多一条比少一条好，不扣分，但精简时可以合并
```

**怎么解的**：

```
1. 修正标注：边界值不等于有效类。a-1 和 b+1 预期拒绝，标 I/边界；
   a, a+1, b-1, b 预期接受，标 边界
2. 补上 E2(纯数字 123456) 和 E3(纯字母 abcdef)，共 13 条
3. I1/I3 保留不合并，实操中覆盖更全
```

**学到的规律**：

```
- 等价类覆盖面，边界值覆盖边缘。先划类再补边
- 无效类比有效类更重要，且必须单独测（一条用例只测一个无效条件）
- 边界值 6 个点：a-1, a, a+1, b-1, b, b+1
- 0 和 1 是最容易被忽略的边界（空字符串、单字符）
- E2(123456) 和边界(6) 是同一个值时可以合并标注 "E2 + 边界(6)"
```

**面试能用**：

- "等价类划分是把输入分成有效和无效若干类，每类取一个代表值。边界值分析是在范围上取边界及±1。两者互补：等价类覆盖面，边界值覆盖边缘。实际设计中我先划等价类，再在每个数值范围上叠加边界值"

**明天第一件事**：W3 Day4 黑盒方法 2——判定表、因果图、场景法、正交实验法、错误推测法
