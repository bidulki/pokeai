from .basic_data_handler import BasicDataHandler

class PokemonDataHandler(BasicDataHandler):
    def __init__(self, data):
        super().__init__(data)
    
    def get_pokemon(self, pokemon_name):
        return self.data[pokemon_name]
    
    def add_message(self, pokemon_name, message):
        pokemon = self.get_pokemon(pokemon_name)
        pokemon.chat_history.append(message)
    
    def add_messages(self, pokemon_name, message_list):
        pokemon = self.get_pokemon(pokemon_name)
        for message in message_list:
            pokemon.chat_history.append(message)