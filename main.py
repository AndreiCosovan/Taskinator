import kivy
from kivy.config import Config
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.picker import MDDatePicker, MDThemePicker
from kivymd.uix.list import IconLeftWidget, IconRightWidget, ThreeLineAvatarIconListItem
from functools import partial
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import uuid
from datetime import datetime
import json



kv_string= '''

FloatLayout:
    cols:1
    BoxLayout:
        orientation:'vertical'
        MDToolbar:
            title: "HOME"
            id: toolbar

        MDBottomNavigation:
            MDBottomNavigationItem:
                name: 'Homescreen'
                text: 'Home'
                icon: 'home-outline'
                on_tab_release:app.change_toolbar("HOME")
                ScrollView:
                    MDList:
                        id: to_do_container
            MDBottomNavigationItem:
                name: 'addToDoScreen'
                text: 'add'
                icon: 'plus-outline'
                on_tab_release:app.change_toolbar("ADD A TASK!")
                MDBoxLayout:
                    orientation: 'vertical'
                    MDTextField:
                        id: input_of_to_do
                        hint_text: "Type in your Task!"
                        pos_hint: {'x': 0, 'y': 0}

                    MDBoxLayout:
                        orientation: 'horizontal'
                        adaptive_height: True
                        MDIconButton:
                            icon: "calendar"
                            on_release: app.show_date_picker()
                        MDLabel:
                            id: date_label
                            text: "No due date picked!"
                            theme_text_color: "Primary"
                            #text_color: app.theme_cls.accent_palette
                    MDBoxLayout:
                        orientation: 'horizontal'
                        adaptive_height: True
                        MDCheckbox:
                            id: important_checkbox
                            size_hint: None, None
                            size: "48dp", "48dp"
                            on_active: app.on_important_checkbox_active(*args)
                        MDLabel:
                            id: important_label
                            text: "Not important!"
                            theme_text_color: "Primary"

                    MDFillRoundFlatButton:
                        text:"ADD"
                        pos_hint: {"center_x": 0.9, "center_y": .5}
                        on_release: app.add_task()
                    MDLabel:
                        text: ""
            MDBottomNavigationItem:
                name: 'statisticsScreen'
                text: 'stats'
                icon: 'clipboard-check'
                on_tab_release:app.change_toolbar("STATISTICS")

                MDBoxLayout:
                    orientation: "vertical"
                    OneLineListItem:
                        text: "Tasks done:"
                        id: tasks_done

                    OneLineListItem:
                        text: "Tasks awaiting:"
                        id: tasks_awaiting

                    OneLineListItem:
                        text: "Most effective weekday:"
                        id: most_effective_weekday
                    
                    MDLabel: 
                        text: ""


            MDBottomNavigationItem:
                name: 'settingsScreen'
                text: 'settings'
                icon: 'settings-outline'
                on_tab_release:app.change_toolbar("SETTINGS")
                MDFloatLayout:
                    MDRaisedButton:
                        text: "Open theme picker"
                        pos_hint: {'center_x': .5, 'center_y': .5}
                        on_release: app.show_theme_picker()

'''





class TaskinatorApp(MDApp):
    dialog = None
    def build(self):
        
        self.root = Builder.load_string(kv_string)

        settings=self.get_settings()
        self.theme_cls.theme_style = settings["mode"]
        self.theme_cls.primary_palette = settings["theme"]
        self.theme_cls.accent_palette=settings["accent"]
        task_list = self.read_tasks()
        self.load_tasks(task_list)       
        self.set_tasks_awaiting(task_list)
        self.set_tasks_done(task_list)
        self.set_most_effective_weekday(task_list)

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        self.root.ids.date_label.text = str(value)

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
            "weekday": "",
            "id": str(uuid.uuid1())
        }
        task_list = self.read_tasks()
        task_list.append(task)
        self.reload_tasks(task_list)     
        self.save_tasks(task_list)
        self.root.ids.input_of_to_do.text=""
        self.root.ids.date_label.text="No due date picked!"
        self.root.ids.important_checkbox.value=False
        
        
    def task_on_release(self, task, kwargs):
        task["is_done"]=True if task["is_done"]==False else False
        weekday=datetime.now().strftime("%A")
        task["weekday"]=weekday if task["is_done"]==True else ""
        #print(task["weekday"])
        self.update_task(task)

    def update_task(self, task_to_change):
        task_list = self.read_tasks()
        for task in task_list:
            if task["id"]==task_to_change["id"]:
                task["is_done"]=task_to_change["is_done"]
                task["weekday"]=task_to_change["weekday"]
                break
        self.save_tasks(task_list)
        self.reload_tasks(task_list)
        

    def read_tasks(self):
        try:
            task_list = list(self.get_tasks())
        except:
            task_list=list()
        return task_list

    def reload_tasks(self, task_list):
        self.root.ids.to_do_container.clear_widgets()
        self.load_tasks(task_list)
        self.set_tasks_awaiting(task_list)
        self.set_tasks_done(task_list)
        self.set_most_effective_weekday(task_list)

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
        self.save_tasks(new_list)
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


    def show_theme_picker(self):
        #before_theme=self.theme_cls.theme_style
        #self.theme_cls.theme_style = "Dark"
        picker = MDThemePicker(on_dismiss=self.save_theme_settings)
        #self.theme_cls.theme_style = before_theme
        picker.open()
        

    def save_theme_settings(self, kwargs):
        settings=dict()
        settings["mode"]=self.theme_cls.theme_style
        settings["theme"]=self.theme_cls.primary_palette
        settings["accent"]=self.theme_cls.accent_palette
        self.save_settings(settings)

    def change_toolbar(self, title):
        self.root.ids.toolbar.title = title

    def set_tasks_awaiting(self, task_list):
        tasks_awaiting=0
        for task in task_list:
            if task["is_done"]==False:
                tasks_awaiting += 1

        self.root.ids.tasks_awaiting.text="Tasks awaiting: {}".format(tasks_awaiting)

    def set_tasks_done(self, task_list):
        tasks_done=0
        for task in task_list:
            if task["is_done"]==True:
                tasks_done += 1

        self.root.ids.tasks_done.text="Tasks done: {}".format(tasks_done)

    def calculate_most_effective_weekday(self, task_list):
        for task in task_list:
            if task["is_done"]==True:
                weekday_list=list()
                weekday_list.append(task["weekday"])
                return max(set(weekday_list), key = weekday_list.count)

            else:
                return "There are no tasks done."
        return "There are no tasks done."

    def set_most_effective_weekday(self, task_list):
        most_effective_weekday=self.calculate_most_effective_weekday(task_list)

        self.root.ids.most_effective_weekday.text="Most effective weekday: {}".format(most_effective_weekday)

    def save_tasks(self, data):
        with open("to_dos.json", "w", encoding='utf-8') as to_dos:
            json.dump(data, to_dos, ensure_ascii=False)

    def get_tasks(self):
        with open("to_dos.json", "r", encoding='utf-8') as to_dos:
            data = json.load(to_dos)
            return data 

    def save_settings(self, data):
        with open("app_settings.json", "w", encoding='utf-8') as settings:
            json.dump(data, settings, ensure_ascii=False) 

    def get_settings(self):
        try:
            with open("app_settings.json", "r", encoding='utf-8') as settings:
                data = json.load(settings)
                return data 
        except:
            self.save_settings({"mode": "Dark", "theme": "Red", "accent": "Pink"})
            return {"mode": "Dark", "theme": "Red", "accent": "Pink"}






if __name__ == '__main__':
    TaskinatorApp().run()



