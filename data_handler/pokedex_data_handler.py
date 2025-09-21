from .basic_data_handler import BasicDataHandler

class PokedexDataHandler(BasicDataHandler):
    def __init__(self, data):
        super().__init__(data)
    
    def get_pokedex(self, pokedex_name):
        return self.data[pokedex_name]
    
    def meet_pokemon(self, pokedex_name):
        pokedex = self.get_pokedex(pokedex_name)
        pokedex['meet'] = True
        return
    
    def catch_pokemon(self, pokedex_name):
        pokedex = self.get_pokedex(pokedex_name)
        pokedex['meet'] = True
        pokedex['catched'] = True
        return