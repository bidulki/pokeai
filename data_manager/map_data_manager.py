from .basic_data_manager import BasicDataManager
from entity import Map
import json
import os

class MapDataManager(BasicDataManager):
    @classmethod
    def load(cls, savedata_dir, gamedata_dir):
        maps = dict()
        if cls.check_savedata_exist(savedata_dir=savedata_dir):
            for save_file_name in os.listdir(savedata_dir):
                save_file_path = os.path.join(savedata_dir, save_file_name)
                with open(save_file_path, 'r', encoding="utf-8") as f:
                    map_data = json.load(f)
                maps[map_data['name']] = Map(map_data)
        else:
            for data_file_name in os.listdir(gamedata_dir):
                data_file_path = os.path.join(gamedata_dir, data_file_name)
                with open(data_file_path, 'r', encoding="utf-8") as f:
                    map_data = json.load(f)
                maps[map_data['name']] = Map(map_data)
        
        return maps
    
    @classmethod
    def save(cls, savedata_dir, map_data):
        os.makedirs(savedata_dir, exist_ok=True)
        for map_name in map_data.keys():
            map = map_data[map_name]
            map_json = map.to_json()
            save_path = os.path.join(savedata_dir, f"{map.name}.json")
            with open(save_path, 'w') as f:
                json.dump(map_json, f, ensure_ascii=False, indent="\t")



        
                
