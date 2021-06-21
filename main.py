import kivy
from kivymd.app import MDApp
kivy.require('2.0.0')  
from kivy.lang import Builder
from kivymd.uix.picker import MDDatePicker, MDThemePicker
from Storage import Storage
from kivymd.uix.list import IconLeftWidget, IconRightWidget, ThreeLineAvatarIconListItem
from functools import partial
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import uuid

storage = Storage()








class to_do_App(MDApp):
    dialog = None
    def build(self):
        self.root = Builder.load_file('to_do_.kv')
        settings=storage.get_settings()
        self.theme_cls.theme_style = settings["mode"]
        self.theme_cls.primary_palette = settings["theme"]
        self.theme_cls.accent_palette=settings["accent"]
        task_list = self.read_tasks()
        self.load_tasks(task_list)       

    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.on_save)
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
            is_important = "Important"
        else:
            is_important = "Not important"
        task = {
            "name": task_name,
            "due_date": due_date,
            "is_important": is_important,
            "is_done": False,
            "id": str(uuid.uuid1())
        }
        task_list = self.read_tasks()
        task_list.append(task)
        self.reload_tasks(task_list)     
        storage.save_data(task_list)
        
    def task_on_release(self, args, kwargs):
        args["is_done"]=True if args["is_done"]==False else False
        self.update_task(args)

    def update_task(self, task_to_change):
        task_list = self.read_tasks()
        for task in task_list:
            if task["id"]==task_to_change["id"]:
                task["is_done"] = task_to_change["is_done"]
                break
        storage.save_data(task_list)
        self.reload_tasks(task_list)

    def read_tasks(self):
        try:
            task_list = list(storage.get_data())
        except:
            task_list=list()
        return task_list

    def reload_tasks(self, task_list):
        self.root.ids.to_do_container.clear_widgets()
        self.load_tasks(task_list)

    def load_tasks(self, task_list):
        for task in task_list:
            
            list_item = ThreeLineAvatarIconListItem(text=task["name"], secondary_text=task["due_date"], tertiary_text=str(task["is_important"]), on_release=partial(self.task_on_release, task))
            remove_icon = IconRightWidget(icon="close", on_release=partial(self.show_remove_task_alert_dialog, task))
            list_item.add_widget(remove_icon)
            check_icon = IconLeftWidget(icon="checkbox-blank-circle", on_release=partial(self.task_on_release, task)) if task["is_done"]==False else IconLeftWidget(icon="checkbox-marked-circle", on_release=partial(self.task_on_release, task))
            list_item.add_widget(check_icon)
            
            self.root.ids.to_do_container.add_widget(list_item)

    def remove_task(self, task, kwargs):
        task_list = self.read_tasks()
        new_list = [i for i in task_list if not (i['id'] == task['id'])]
        storage.save_data(new_list)
        self.reload_tasks(new_list)
        self.close_dialog(None)

    def close_dialog(self, kwargs):
        self.dialog.dismiss()
        
        

    def show_remove_task_alert_dialog(self, task, kwargs):
        self.dialog = MDDialog(
            text="Remove task?",
            buttons=[
                MDFlatButton(
                    text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="REMOVE", text_color=self.theme_cls.primary_color, on_release=partial(self.remove_task, task)
                ),
            ],
            size_hint=(0.7, 1)
        )
        self.dialog.open()

    # def change_mode(self, checkbox, value):

    #     if value:
    #         self.theme_cls.theme_style = "Light" 
    #     else:
    #         self.theme_cls.theme_style = "Dark"

    def show_theme_picker(self):
        before_theme=self.theme_cls.theme_style
        self.theme_cls.theme_style = "Dark"
        picker = MDThemePicker(on_dismiss=self.save_settings)
        self.theme_cls.theme_style = before_theme
        picker.open()
        

    def save_settings(self, kwargs):
        settings=dict()
        settings["mode"]=self.theme_cls.theme_style
        settings["theme"]=self.theme_cls.primary_palette
        settings["accent"]=self.theme_cls.accent_palette
        storage.save_settings(settings)




if __name__ == '__main__':
    to_do_App().run()



