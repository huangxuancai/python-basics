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

todos=load_todos()

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
        save_todos(todos)
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
        save_todos(todos)
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
        save_todos(todos)
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