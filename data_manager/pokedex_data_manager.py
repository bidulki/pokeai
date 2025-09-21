from .basic_data_manager import BasicDataManager
import json
import os

class PokedexDataManager(BasicDataManager):
    @classmethod
    def load(cls, savedata_dir, gamedata_dir):
        pokedexs = dict()
        if cls.check_savedata_exist(savedata_dir=savedata_dir):
            for save_file_name in os.listdir(savedata_dir):
                save_file_path = os.path.join(savedata_dir, save_file_name)
                with open(save_file_path, 'r', encoding="utf-8") as f:
                    pokedex_data = json.load(f)
                pokedexs[pokedex_data['name']] = pokedex_data
        else:
            for data_file_name in os.listdir(gamedata_dir):
                data_file_path = os.path.join(gamedata_dir, data_file_name)
                with open(data_file_path, 'r', encoding="utf-8") as f:
                    pokedex_data = json.load(f)
                pokedexs[pokedex_data['name']] = pokedex_data

        return pokedexs
    
    @classmethod
    def save(cls, savedata_dir, pokedex_data):
        os.makedirs(savedata_dir, exist_ok=True)
        for key in pokedex_data.keys():
            pokedex = pokedex_data[key]
            save_path = os.path.join(savedata_dir, f"{pokedex['name']}.json")
            with open(save_path, 'w') as f:
                json.dump(pokedex, f, ensure_ascii=False, indent="\t")
    
