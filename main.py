import kivy
from kivymd.app import MDApp
from WindowManager import WindowManager
kivy.require('2.0.0')  # replace with your current kivy version !
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from WindowManager import WindowManager
from screens import MainWindow
from kivymd.uix.picker import MDDatePicker
from Storage import Storage
from Task import Task
from kivymd.uix.list import IconLeftWidget, ThreeLineIconListItem
#kv = Builder.load_file("to_do_.kv")
sm = WindowManager()
storage = Storage()
#screens = [MainWindow.MainWindow(name="MainWindow")]
#for screen in screens:
#    sm.add_widget(screen)
#sm.current = "MainWindow"








class to_do_App(MDApp):
    def build(self):
        self.root = Builder.load_file('to_do_.kv')
        self.theme_cls.theme_style = "Dark"
        #showing tasks
        try:
            task_list = list(storage.get_data())
        except:
            task_list=list()
        for task in task_list:
            
            list_item = ThreeLineIconListItem(text=task["name"], secondary_text=task["due_date"], tertiary_text=str(task["is_important"]))
            icon = IconLeftWidget(icon="checkbox-blank-circle") if task["is_done"]==False else IconLeftWidget(icon="checkbox.marked-circle")
            list_item.add_widget(icon)
            self.root.ids.to_do_container.add_widget(list_item)
        

    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.on_save)
        #date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, date):
        self.root.ids.date_label.text = str(date)

    def on_important_checkbox_active(self, checkbox, value):
        if value:
            self.root.ids.important_label.text = "Important!"
        else:
            self.root.ids.important_label.text = "Not important!"

    def add_task(self):
        task_name = self.root.ids.input_of_to_do.text
        due_date = self.root.ids.date_label.text
        if self.root.ids.important_label.text == "Important!":
            is_important = True
        else:
            is_important = False
        task = {
            "name": task_name,
            "due_date": due_date,
            "is_important": is_important,
            "is_done": False
        }
        try:
            task_list = list(storage.get_data())
        except:
            task_list=list()
        task_list.append(task)
        #updating tasks
        self.root.ids.to_do_container.clear_widgets()
        for task in task_list:
            list_item = ThreeLineIconListItem(text=task["name"], secondary_text=task["due_date"], tertiary_text=str(task["is_important"]))
            icon = IconLeftWidget(icon="checkbox-blank-circle") if task["is_done"]==False else IconLeftWidget(icon="checkbox.marked-circle")
            list_item.add_widget(icon)
            self.root.ids.to_do_container.add_widget(list_item)
            # self.root.ids.to_do_container.add_widget(
            #     ThreeLineIconListItem(text=task["name"], secondary_text=task["due_date"], tertiary_text=str(task["is_important"]))
            # )
        storage.add_data(task_list)
        

    def update_tasks(self):
        task_list = storage.get_data()
        for task in task_list:
            self.root.ids.to_do_container.add_widget(
                ThreeLineIconListItem(text=task["name"], secondary_text=task["due_date"], tertiary_text=task["is_important"], icon="checkbox-blank")
            )

        







if __name__ == '__main__':
    to_do_App().run()
