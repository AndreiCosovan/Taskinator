import json


def save(self, data):
    with open("to_dos.json", "w") as to_dos:
        json.dump(data, to_dos)


def update(self):
    with open("to_dos.json", "r") as to_dos:
        data = json.load(to_dos)
        return data 
