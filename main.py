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

#kv = Builder.load_file("to_do_.kv")
sm = WindowManager()
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
        print(date)





if __name__ == '__main__':
    to_do_App().run()
