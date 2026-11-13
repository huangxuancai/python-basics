# python-basics

从零开始的 Python 学习仓库（2026-11 起持续更新）。

## todo.py —— 命令行待办事项工具

一个用纯标准库写的待办清单：数据存在 todo.txt，重启不丢。

### 怎么跑

    python todo.py        # 需要 Python 3.10+

### 功能

- 添加 / 列出 / 标记完成 / 删除待办
- 完成进度统计
- 数据持久化（todo.txt），文件不存在或损坏时安全降级为空列表
- 输入校验：非数字、越界编号都有提示，不会崩溃

### 代码结构

| 函数                                        | 职责                                  |
| ------------------------------------------- | ------------------------------------- |
| load_todos()                                | 读 todo.txt，文件缺失返回 []          |
| save_todos(todos)                           | 每次改动后整体写回                    |
| ask_index(prompt, todos)                    | 输入编号 + 校验，返回 0 基下标或 None |
| print_menu() / print_todos() / show_stats() | 界面输出                              |

### 踩过的坑（DAILY.md 里有完整记录）

- `sort()` 返回 None，`print(lst.sort())` 静默失效
- `int(input())` 合并成一行时把类型转换挤出了 try，非法输入直接崩
- 文件读写两端必须都写 `encoding="utf-8"`（Windows 默认 cp936）
- 遍历字典时增删 key 会 RuntimeError，先 `list(d)` 固化

## 学习记录

- `day4_practice.py` ~ `day6_practice.py`：每日练习
- `dict_drill.py`：字典专项 22 题
- `DAILY.md`：每日复盘（卡点 + 解决过程）