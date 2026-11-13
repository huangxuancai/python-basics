TODO_FILE = "todo.txt"

class Todo:
    def __init__(self, title, done=False):
        self.title=title
        self.done=done

    def mark_done(self):
        self.done=True

    def to_line(self):
        return f"{self.title},{1 if self.done else 0}"

    @classmethod
    def from_line(cls, line):
        row = line.strip().split(",")
        if len(row) < 2:
            return None
        return cls(row[0], row[1] == "1")

    def __str__(self):
        mark = "[x]" if self.done else "[ ]"
        return f"{mark} {self.title}"

def load_todos():      # 启动时读：文件不存在就返回空列表
    try:
        with open(TODO_FILE,encoding="utf-8") as f:
            lines=f.readlines()
    except FileNotFoundError: return []
    return [Todo.from_line(l) for l in lines if Todo.from_line(l)]

def save_todos(todos): # 每次改动后写回
    with open(TODO_FILE,"w",encoding="utf-8") as f:
        for t in todos:
            f.write(t.to_line()+"\n")

def ask_index(prompt, todos):
    """提示输入编号，校验后返回 0 基下标；输入非法返回 None。

    参数: prompt 提示语, todos 当前列表（用来判断越界）
    返回: int 下标 或 None
    """
    if not todos:
        print("暂无事项可操作")
        return None

    temp = input(prompt)
    try:
        index=int(temp)-1
    except ValueError:
        print("输入无效，请输入数字:")
        return None

    if index <0 or index >=len(todos):
        print("输入编号无效!")
        return None

    return index

def print_menu():
    """打印一次菜单"""
    print("\n =====代办事项=====")
    print("1 添加  2 列出  3 标记完成  4 删除  5展示进度 q 退出")

def print_todos(todos):
    """打印当前列表:空列表给提示."""
    if not todos:
        print("(暂无事项)")
        return
    for i,todo in enumerate(todos,start=1):
        print(f"{i}. {todo}")
          
def show_stats(todos):
    """打印完成进度：已完成 x / 共 y。"""
    print(f"进度: {sum(1 for t in todos if t.done)}/{len(todos)} 已完成")

todos=load_todos()
print_todos(todos)

while True:
    print_menu()
    choice=input("请输入你的选项:")
    if choice == "1":
        add_title=input("请输入你需要添加的代办事项:")
        todos.append(Todo(add_title))
        save_todos(todos)
        
    
    elif choice == "3":
        finish_index=ask_index("请输入你已完成事项的编号:",todos)
        if finish_index is None:
            continue
        todos[finish_index].mark_done()
        save_todos(todos)
        print("已标记完成")
        
    
    elif choice == "4":
        del_index = ask_index("请输入你要删除的事项编号:",todos)
        if del_index is None:
            continue
        todos.pop(del_index)
        save_todos(todos)
        print("已删除")
        
    
    elif choice == "2":
        print_todos(todos)

    elif choice == "5":
        show_stats(todos)
    
    elif choice == "q":
        break
    
    else:
        print("输入有误,请重新输入!")
        