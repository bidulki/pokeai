from prompts import POKEMON_INFO_PROMPT
import json
import os

class Pokemon:
    def __init__(self, poke_info):
        self.id = poke_info.id
        self.dexNum = poke_info.dexNum
        self.hp = poke_info.hp
        self.status = poke_info.status
        self.poke_info = poke_info
        self.load_pokedex()

    def load_pokedex(self):
        pokedex_file_path = os.path.join("./pokedex/information", f"{self.dexNum}.json")
        with open(pokedex_file_path, 'r', encoding='UTF8') as f:
            pokedex_json = json.load(f)

        self.image_path = pokedex_json['image']
        self.name = pokedex_json['name']
        self.category = pokedex_json['category']
        self.description = pokedex_json['description']
        self.types = ", ".join(pokedex_json['type'])
        self.height = pokedex_json['height']
        self.weight = pokedex_json['weight']

        self.info = POKEMON_INFO_PROMPT.format(
            name=self.name,
            category=self.category,
            description=self.description,
            types=self.types,
            height=self.height,
            weight=self.weight,
            hp = self.hp,
            status = self.status
        )