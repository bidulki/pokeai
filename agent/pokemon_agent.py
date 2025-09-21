from agent import Agent
from character import Pokemon
from data_handler import DataHandler
from format import pokemon_format
from tools import pokemon_tools
from prompts import *

class PokemonAgent(Agent):
    def __init__(self, pokemon: Pokemon, data_handler: DataHandler):
        super().__init__()
        self.data_handler = data_handler
        self.character = pokemon
        self.chat_history = pokemon.chat_history.copy()

    def get_system_prompt(self):
        return POKEMON_SYSTEM_PROMPT

    def speak(self):
        messages = self.chat_history
        pokemon = self.character
        map = self.data_handler.map.get_map(pokemon.map)

        character_list = self.data_handler.map.get_characters(map.name)
        character_list = list(character_list.keys())
        
        messages += [self.make_message(role="user", content=POKEMON_SPEAK_PROMPT.format(
            pokemon_name = pokemon.name,
            pokemon_info = "\n".join(pokemon.description),
            map_name = map.name,
            map_info = map.info,
            character_list = character_list
        ))]

        if self.provider == "openai":
            output = self.get_response_structured_output(messages, pokemon_format.speak(
                pokemon_name = pokemon.name,
                character_list= character_list
            ))
            if output.action.type == "speak":
                action = {
                    "type": "speak",
                    "name": output.action.name,
                    "chat": output.action.chat,
                    "target": output.action.target
                }
        elif self.provider == "anthropic":
            action = self.get_response_function_calling(messages, pokemon_tools.speak(
                pokemon_name = pokemon.name,
                character_list = character_list,
                provider = self.provider
            ))
            if action.name == "speak":
                action = {
                    "type": "speak",
                    "name": action.input['name'],
                    "chat": action.input['chat'],
                    "target": action.input['target']
                }
        elif self.provider == "google":
            action = self.get_response_function_calling(messages, pokemon_tools.speak(
                pokemon_name = pokemon.name,
                character_list = character_list,
                provider = self.provider
            ))
            if action.name == "speak":
                action = {
                    "type": "speak",
                    "name": action.args['name'],
                    "chat": action.args['chat'],
                    "target": action.args['target']
                }
        return action
