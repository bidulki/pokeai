import os
import json
from prompts import ITEM_INFO_PROMPT

class Item:
    def __init__(self, itemId):
        self.id = itemId
        self.load_item_info(itemId)

    def load_item_info(self, itemId):
        item_path = os.path.join("./items", f"{itemId}.json")
        with open(item_path, 'r', encoding='UTF8') as f:
            item_json = json.load(f)
        self.name = item_json['name']
        self.price = item_json['price']
        self.description = item_json['description']

        self.info = ITEM_INFO_PROMPT.format(
            name=self.name,
            description=self.description,
            price=self.price
        )