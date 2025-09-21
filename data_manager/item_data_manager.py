from .basic_data_manager import BasicDataManager
from entity import Ball, Stone, Restore, Special
import json
import os

class ItemDataManager(BasicDataManager):
    @classmethod
    def load(cls, gamedata_dir):
        items = dict()
        items = cls.load_ball(os.path.join(gamedata_dir, "ball"), items)
        items = cls.load_stone(os.path.join(gamedata_dir, "stone"), items)
        items = cls.load_restore(os.path.join(gamedata_dir, "restore"), items)
        items = cls.load_special(os.path.join(gamedata_dir, "special"), items)

        return items
    
    @classmethod
    def load_ball(cls, gamedata_dir, items):
        for data_file_name in os.listdir(gamedata_dir):
            data_file_path = os.path.join(gamedata_dir, data_file_name)
            with open(data_file_path, 'r', encoding="utf-8") as f:
                ball_data = json.load(f)
            items[ball_data['name']] = Ball(ball_data)
        return items
    
    @classmethod
    def load_stone(cls, gamedata_dir, items):
        for data_file_name in os.listdir(gamedata_dir):
            data_file_path = os.path.join(gamedata_dir, data_file_name)
            with open(data_file_path, 'r', encoding="utf-8") as f:
                stone_data = json.load(f)
            items[stone_data['name']] = Stone(stone_data)
        return items
    
    @classmethod
    def load_restore(cls, gamedata_dir, items):
        for data_file_name in os.listdir(gamedata_dir):
            data_file_path = os.path.join(gamedata_dir, data_file_name)
            with open(data_file_path, 'r', encoding="utf-8") as f:
                restore_data = json.load(f)
            items[restore_data['name']] = Restore(restore_data)
        return items
    
    @classmethod
    def load_special(cls, gamedata_dir, items):
        for data_file_name in os.listdir(gamedata_dir):
            data_file_path = os.path.join(gamedata_dir, data_file_name)
            with open(data_file_path, 'r', encoding="utf-8") as f:
                special_data = json.load(f)
            items[special_data['name']] = Special(special_data)
        return items
