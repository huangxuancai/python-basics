TODO_FILE = "todo.txt"

def load_todos():      # 启动时读：文件不存在就返回空列表
    result=[]
    try:
        with open(TODO_FILE,encoding="utf-8") as f:
            lines=f.readlines()
    except FileNotFoundError: return []
    for line in lines:
        row=line.strip().split(",")
        if len(row) < 2:
            continue
        result.append({"title":row[0],"done":row[1]=="1"})

    return result

def save_todos(todos): # 每次改动后写回
    with open(TODO_FILE,"w",encoding="utf-8") as f:
        for t in todos:
            f.write(t["title"]+",")
            if t["done"]:
                f.write("1"+"\n")
            else:
                f.write("0"+"\n")

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
    print("1 添加  2 列出  3 标记完成  4 删除  q 退出")

def print_todos(todos):
    """打印当前列表:空列表给提示."""
    if not todos:
        print("(暂无事项)")
        return
    for i,todo in enumerate(todos,start=1):
        mark = "[x]" if todo["done"] else "[ ]"
        print(f"{i}.{mark} {todo['title']}")
          
def show_stats(todos):
    """打印完成进度：已完成 x / 共 y。"""
    done_count=0
    for todo in todos:
        if todo["done"]:
            done_count+=1
    print(f"进度: {done_count}/{len(todos)} 已完成")

todos=load_todos()
print_todos(todos)

while True:
    print_menu()
    choice=input("请输入你的选项:")
    if choice == "1":
        add_title=input("请输入你需要添加的代办事项:")
        todos.append({"title":add_title,"done":False})
        save_todos(todos)
        
    
    elif choice == "3":
        finish_index=ask_index("请输入你已完成事项的编号:",todos)
        if finish_index is None:
            continue
        todos[finish_index]["done"]=True
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
        