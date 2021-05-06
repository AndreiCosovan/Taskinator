class Task:
    def __init__(self, task_name, due_date, is_important):
        self.task_name = task_name
        self.due_date = due_date
        self.is_important = is_important
        self.is_done = False