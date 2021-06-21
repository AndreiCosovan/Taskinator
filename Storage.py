import json

class Storage:
    def save_data(self, data):
        with open("to_dos.json", "w", encoding='utf-8') as to_dos:
            json.dump(data, to_dos, ensure_ascii=False)


    def get_data(self):
        with open("to_dos.json", "r", encoding='utf-8') as to_dos:
            data = json.load(to_dos)
            return data 

    def save_settings(self, data):
       with open("app_settings.json", "w", encoding='utf-8') as settings:
            json.dump(data, settings, ensure_ascii=False) 

    def get_settings(self):
       with open("app_settings.json", "r", encoding='utf-8') as settings:
            data = json.load(settings)
            return data 