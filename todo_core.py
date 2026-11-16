"""todo 的数据层：Todo 类 + 文件存取。"""
from todo_errors import TodoError, InvalidIndexError, EmptyTitleError

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

def add_todo(todos, title):
    if not title.strip():
        raise EmptyTitleError("标题不能为空")
    todos.append(Todo(title.strip()))

def get_todo(todos, idx):
    if idx < 0 or idx >= len(todos):
        raise InvalidIndexError(f"下标 {idx} 越界(共{len(todos)}条)")
    return todos[idx]

if __name__ == "__main__":
    # 数据层自检：直接跑这个文件时测一轮存取
    ts = load_todos()
    print(f"[todo_core 自检] 读到 {len(ts)} 条:", ts)