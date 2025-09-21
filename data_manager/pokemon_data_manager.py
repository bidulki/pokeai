from .basic_data_manager import BasicDataManager
from character import Pokemon
import json
import os

class PokemonDataManager(BasicDataManager):
    @classmethod
    def load(cls, savedata_dir, gamedata_dir):
        pokemons = dict()
        if cls.check_savedata_exist(savedata_dir=savedata_dir):
            for save_file_name in os.listdir(savedata_dir):
                save_file_path = os.path.join(savedata_dir, save_file_name)
                with open(save_file_path, 'r', encoding="utf-8") as f:
                    pokemon_data = json.load(f)
                pokemon = Pokemon()
                pokemon.load_pokemon(pokemon_data)
                pokemons[pokemon.name] = pokemon
        else:
            for data_file_name in os.listdir(gamedata_dir):
                data_file_path = os.path.join(gamedata_dir, data_file_name)
                with open(data_file_path, 'r', encoding="utf-8") as f:
                    pokemon_data = json.load(f)
                pokemon = Pokemon()
                pokemon.load_pokemon(pokemon_data)
                pokemons[pokemon.name] = pokemon  
        
        return pokemons
    
    @classmethod
    def save(cls, savedata_dir, pokemon_data):
        os.makedirs(savedata_dir, exist_ok=True)
        for key in pokemon_data.keys():
            pokemon = pokemon_data[key]
            pokemon_json = pokemon.to_json()
            save_path = os.path.join(savedata_dir, f"{pokemon.name}.json")
            with open(save_path, 'w') as f:
                json.dump(pokemon_json, f, ensure_ascii=False, indent="\t")
    
