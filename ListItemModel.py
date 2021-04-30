from datetime import datetime

class ListItemModel:
    def __init__(self, text, due_date, is_important, is_done):
        self.text = text
        self.due_date = due_date
        self.is_important = is_important
        self.is_done = is_done
        self.time_when_done = None

    def done(self):
        self.time_when_done = datetime.now()
