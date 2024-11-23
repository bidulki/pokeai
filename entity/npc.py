from prompts import NPC_INFO_PROMPT
from .pokemon import Pokemon
import json
import os

class NPC:
    def __init__(self, npc_info):
        self.npc_info = npc_info
        self.load_npc_info(npc_info.id)
        self.load_pokemon(npc_info.pokeList)

    def load_npc_info(self, npc_id):
        npc_file_path = os.path.join("./npc_persona", f"{npc_id}.json")
        with open(npc_file_path, 'r') as f:
            npc_json = json.load(f)

        self.id = npc_json['id']
        self.name = npc_json['name']
        self.sex = npc_json['sex']
        self.age = npc_json['age']
        self.job = npc_json['job']
        self.birthplace = npc_json['birthplace']
        self.family = npc_json['family']
        self.persona = npc_json['persona']

        self.info = NPC_INFO_PROMPT.format(
            name=self.name,
            sex=self.sex,
            age=self.age,
            job=self.job,
            birthplace=self.birthplace,
            family="\n".join(self.family),
            persona="\n".join(self.persona)
        )
    
    def load_pokemon(self, pokemon_list):
        self.pokemon_list = []
        if len(pokemon_list) >0:
            for poke_info in pokemon_list:
                pokemon = Pokemon(poke_info)
                self.pokemon_list.append(pokemon)
    