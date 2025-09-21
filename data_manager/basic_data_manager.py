import os

class BasicDataManager:
    @classmethod
    def check_savedata_exist(cls, savedata_dir):
        if os.path.isdir(savedata_dir):
            return True
        else:
            return False