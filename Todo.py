class Todo:
    count_id = 0

    def __init__(self, todo_text, todo_date):
        Todo.count_id += 1
        self.__todo_id = Todo.count_id
        self.__todo_text = todo_text
        self.__todo_date = todo_date

    def get_todo_id(self):
        return self.__todo_id

    def get_todo_text(self):
        return self.__todo_text

    def set_todo_text(self, todo_text):
        self.__todo_text = todo_text

    def get_todo_date(self):
        return self.__todo_date

    def set_todo_date(self, todo_date):
        self.__todo_date = todo_date
