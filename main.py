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

        task = [task_name, due_date, is_important]
        storage.add_data(task)

        







if __name__ == '__main__':
    to_do_App().run()
