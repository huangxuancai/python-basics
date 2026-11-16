#   1. 建 todo_errors.py,搬三个异常类
#   todo_errors.py  ← TodoError / InvalidIndexError / EmptyTitleError

class TodoError(Exception):
    """todo 项目所有业务异常的基类。"""

class InvalidIndexError(TodoError):
    """编号越界。"""

class EmptyTitleError(TodoError):
    """标题为空。"""
