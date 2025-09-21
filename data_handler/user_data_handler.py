from .basic_data_handler import BasicDataHandler

class UserDataHandler(BasicDataHandler):
    def __init__(self, data):
        super().__init__(data)

    def get_name(self):
        return self.data.name
    
    def get_map(self):
        return self.data.map
    
    def get_money(self):
        return self.data.money
    
    def get_pokemon_list(self):
        return self.data.pokemon_list
    
    def get_inventory(self):
        return self.data.inventory
    
    def set_map(self, map_key):
        self.data.map = map_key
