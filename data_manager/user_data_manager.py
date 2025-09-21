from .basic_data_manager import BasicDataManager
from character import User
import json
import os

class UserDataManager(BasicDataManager):
    @classmethod
    def load(cls, savedata_dir):
        if cls.check_savedata_exist(savedata_dir=savedata_dir):
            save_path = os.path.join(savedata_dir, "user.json")
            with open(save_path, 'r', encoding="utf-8") as f:
                user_data = json.load(f)
            user = User()
            user.set_from_data(user_data)
        else:
            user = User()
            user.set_default()

        return user

    @classmethod
    def save(cls, savedata_dir, user):
        user_json = user.to_json()

        os.makedirs(savedata_dir, exist_ok=True)
        save_path = os.path.join(savedata_dir, "user.json")
        
        with open(save_path, 'w') as f:
            json.dump(user_json, f, ensure_ascii=False, indent="\t")
