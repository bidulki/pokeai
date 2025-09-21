import json
import os

class Move:
    def __init__(self, move_name):
        move_path = os.path.join("./gamedata/move", f"{move_name}.json")
        with open(move_path, "r", encoding="utf-8") as f:
            move_data = json.load(f)
        self.load_move(move_data)

    def load_move(self, move_data):
        self.name = move_data['name']
        self.type = move_data['type']
        self.category = move_data['category']
        self.power = move_data['power']
        self.accuracy = move_data['accuracy']
        self.never_miss = move_data['never_miss']
        self.description = move_data['description']
    
    def get_info(self):
        move_info = f"{self.name}\n"
        move_info += f"타입: {self.type}\n"
        move_info += f"분류: {self.category}\n"
        move_info += f"위력: {self.power}\n"
        move_info += f"명중률: {self.accuracy}\n"
        move_info += f"효과: {self.description}\n\n"
        return move_info

    def to_json(self):
        move_data = {
            "name": self.name,
            "type": self.type,
            "category": self.category,
            "power": self.power,
            "accuracy": self.accuracy,
            "never_miss": self.never_miss,
            "description": self.description
        }
        return move_data