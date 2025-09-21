from agent import Agent
from format import npc_format
from tools import npc_tools
from prompts.npc_prompt import *
from data_handler import DataHandler
from character import NPC
import os

class NPCAgent(Agent):
    def __init__(self, npc: NPC, data_handler: DataHandler):
        super().__init__()
        self.data_handler = data_handler
        self.character = npc
        self.chat_history = npc.chat_history.copy()
        self.load_pokemon()

    def get_system_prompt(self):
        return NPC_SYSTEM_PROMPT
    
    def load_pokemon(self):
        pokemon_list = []
        for pokemon_name in self.character.pokemon_list:
            pokemon = self.data_handler.pokemon.get_pokemon(pokemon_name)
            pokemon_list.append(pokemon)
        self.pokemon_list = pokemon_list
    
    def get_inventory_info(self):
        inventory_info = f"현재 {self.character.name}의 인벤토리에는 다음과 같은 아이템이 있습니다.\n"
        for item in self.character.inventory:
            inventory_info += f"{item[0]}: {item[1]}개\n"
            item_info = self.data_handler.item.get_info(item[0])
            inventory_info += f"{item_info}\n"
        return inventory_info
    
    def choose_action(self):
        npc = self.character
        map = self.data_handler.map.get_map(npc.map)
        
        character_list = self.data_handler.map.get_characters(map.name)
        character_list = list(character_list.keys())

        untalkable_character_list = []
        talkable_character_list = []
        for character_name in character_list:
            talkable = self.data_handler.check_talkable(npc.map, npc.name, character_name, 5)
            if talkable:
                talkable_character_list.append(character_name)
            else:
                untalkable_character_list.append(character_name)
        
        map_list = self.data_handler.map.get_map_list()
        map_list.remove(npc.map)
        spot_list = []
        for spot in self.data_handler.map.get_spots(npc.map):
            touchable = self.data_handler.check_talkable(npc.map, npc.name, spot, 1)
            if touchable==False:
                spot_list.append(spot)

        # 소유한 배틀가능한 포켓몬이 있는지 확인
        battle_available = False
        for pokemon in self.pokemon_list:
            if pokemon.status != "기절":
                battle_available = True
                break

        messages = [self.make_message(role="user", content=NPC_ACTION_PROMPT.format(
            npc_name = npc.name,
            npc_info = "\n".join(npc.info),
            map_name = map.name,
            map_info = map.info,
            untalkable_character_list = untalkable_character_list,
            talkable_character_list = talkable_character_list,
            map_list = map_list,
            spot_list = spot_list,
            item_list = npc.get_item_list(),
            inventory_info = self.get_inventory_info(),
            pokemon_list = npc.pokemon_list
        ))]

        messages += self.chat_history
       
        if self.provider=="openai":
            output = self.get_response_structured_output(messages, npc_format.choose_action(
                npc_name = npc.name,
                character_list = character_list,
                pokemon_list = npc.pokemon_list,
                item_list = npc.get_item_list()
            ))
            if output.action.type == "speak":
                action = {
                    "type": "speak",
                    "name": output.action.name,
                    "target": output.action.target,
                    "chat": output.action.chat
                }
            elif output.action.type == "give_pokemon":
                action = {
                    "type": "give_pokemon",
                    "name": output.action.name,
                    "target": output.action.target,
                    "pokemon": output.action.pokemon,
                    "chat": output.action.chat
                }
            elif output.action.type == "give_item":
                action = {
                    "type": "give_item",
                    "name": output.action.name,
                    "target": output.action.target,
                    "item": output.action.item,
                    "num": output.action.num,
                    "chat": output.action.chat
                }
        elif self.provider=="anthropic":
            action = self.get_response_function_calling(messages, npc_tools.choose_action(
                npc_name = npc.name,
                character_list = character_list,
                pokemon_list = npc.pokemon_list,
                item_list = npc.get_item_list(),
                provider = self.provider
            ))
            if action.name == "speak":
                action = {
                    "type": "speak",
                    "name": action.input['name'],
                    "target": action.input['target'],
                    "chat": action.input['chat']
                }
            elif action.name == "give_pokemon":
                action = {
                    "type": "give_pokemon",
                    "name": action.input['name'],
                    "target": action.input['target'],
                    "pokemon": action.input['pokemon'],
                    "chat": action.input['chat']
                }
            elif action.name == "give_item":
                action = {
                    "type": "give_item",
                    "name": action.input['name'],
                    "target": action.input['target'],
                    "item": action.input['item'],
                    "num": action.input['num'],
                    "chat": action.input['chat']
                }
        elif self.provider=="google":
            tools = npc_tools.choose_action(
                npc_name = npc.name,
                untalkable_character_list = untalkable_character_list,
                talkable_character_list = talkable_character_list,
                map_list = map_list,
                spot_list = spot_list,
                pokemon_list = npc.pokemon_list,
                item_list = npc.get_item_list(),
                battle_available = battle_available,
                provider = self.provider
            )
            for tool in tools:
                print(tool["name"], end=", ")
            print()
            action = self.get_response_function_calling(messages, tools)
            if action.name == "speak":
                action = {
                    "type": "speak",
                    "name": action.args['name'],
                    "target": action.args['target'],
                    "chat": action.args['chat']
                }
            elif action.name == "give_pokemon":
                action = {
                    "type": "give_pokemon",
                    "name": action.args['name'],
                    "target": action.args['target'],
                    "pokemon": action.args['pokemon'],
                    "chat": action.args['chat']
                }
            elif action.name == "give_item":
                action = {
                    "type": "give_item",
                    "name": action.args['name'],
                    "target": action.args['target'],
                    "item": action.args['item'],
                    "num": action.args['num'],
                    "chat": action.args['chat']
                }
            elif action.name == "call_character":
                action = {
                    "type": "call_character",
                    "name": action.args['name'],
                    "target": action.args['target'],
                    "chat": action.args['chat']
                }
            elif action.name == "move_map":
                #이동한 맵의 spot을 선택해야함
                spot_list = list(self.data_handler.map.get_spots(action.args['map']).keys())
                # 캐릭터들의 위치도 spot에 포함
                spot_list += list(self.data_handler.map.get_characters(action.args['map']).keys())
                print(spot_list)
                spot_tool = npc_tools.move_spot(
                    npc_name = npc.name,
                    spot_list = spot_list,
                    provider = self.provider
                )
                spot = self.get_response_function_calling(messages, [spot_tool])
                action = {
                    "type": "move_map",
                    "name": action.args['name'],
                    "map": action.args['map'],
                    "spot": spot.args['spot'],
                    "behavior": action.args['behavior']
                }
            elif action.name == "move_spot":
                action = {
                    "type": "move_spot",
                    "name": action.args['name'],
                    "spot": action.args['spot'],
                    "behavior": action.args['behavior']
                }
            elif action.name == "initiate_battle":
                action = {
                    "type": "initiate_battle",
                    "name": action.args['name'],
                    "target": action.args['target'],
                    "chat": action.args['chat']
                }
            

        return action
        

        