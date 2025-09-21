from .basic_data_manager import BasicDataManager
from character import NPC
import json
import os

class NPCDataManager(BasicDataManager):
    @classmethod
    def load(cls, savedata_dir, gamedata_dir):
        npcs = dict()
        if cls.check_savedata_exist(savedata_dir=savedata_dir):
            for save_file_name in os.listdir(savedata_dir):
                save_file_path = os.path.join(savedata_dir, save_file_name)
                with open(save_file_path, 'r', encoding="utf-8") as f:
                    npc_data = json.load(f)
                npcs[npc_data['name']] = NPC(npc_data)
        else:
            for data_file_name in os.listdir(gamedata_dir):
                data_file_path = os.path.join(gamedata_dir, data_file_name)
                with open(data_file_path, 'r', encoding="utf-8") as f:
                    npc_data = json.load(f)
                npcs[npc_data['name']] = NPC(npc_data)

        return npcs
    
    @classmethod
    def save(cls, savedata_dir, npc_data):
        os.makedirs(savedata_dir, exist_ok=True)
        for key in npc_data.keys():
            npc = npc_data[key]
            npc_json = npc.to_json()
            save_path = os.path.join(savedata_dir, f"{npc.name}.json")
            with open(save_path, "w") as f:
                json.dump(npc_json, f, ensure_ascii=False, indent="\t")