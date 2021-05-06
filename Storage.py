import json

class Storage:
    def add_data(self, data):
        with open("to_dos.json", "w", encoding='utf-8') as to_dos:
            json.dump(data, to_dos, ensure_ascii=False)


    def get_data(self):
        with open("to_dos.json", "r", encoding='utf-8') as to_dos:
            data = json.load(to_dos)
            return data 
