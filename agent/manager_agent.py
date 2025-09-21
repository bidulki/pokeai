from prompts import *
from format import manager_format
from tools import manager_tools
from agent import Agent
from .npc_agent import NPCAgent
from .pokemon_agent import PokemonAgent
from data_handler import DataHandler
import os
from utils import josa
import json

class AgentManager(Agent):
    def __init__(self, savedata_dir, data_handler: DataHandler):
        log_dir = os.path.join(savedata_dir, "manager")
        os.makedirs(log_dir, exist_ok=True)
        self.log_path = os.path.join(log_dir, "log.jsonl")
        super().__init__()
        if not os.path.exists(self.log_path):
            self.chat_history = []
        else:
            self.load_log()
        self.data_handler= data_handler

    def save_log(self):
        #save with jsonl format
        with open(self.log_path, "w") as f:
            for message in self.chat_history:
                f.write(json.dumps(message, ensure_ascii=False) + "\n")

    def load_log(self):
        #load with jsonl format
        self.chat_history = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                message = json.loads(line)
                self.chat_history.append(message)   
    
    def get_system_prompt(self):
        return MANAGER_SYSTEM_PROMPT
    
    def add_messages_in_range(self, message_list, map_name=None):
        if map_name == None:
            in_range_characters = self.data_handler.get_current_map_characters_list()
        else:
            in_range_characters = list(self.data_handler.map.get_characters(map_name).keys())
        
        for character_name in in_range_characters:
            type = self.data_handler.get_type_by_name(character_name)
            if type == "npc":
                self.data_handler.npc.add_messages(character_name, message_list)
            if type == "pokemon":
                self.data_handler.pokemon.add_messages(character_name, message_list)
    
    def get_npc_and_pokemon_list(self):
        character_list = []
        for character in self.data_handler.get_current_map_characters_list():
            if character != self.data_handler.user.get_name():
                character_list.append(character)
        return character_list
    
    def get_characters_info(self):
        character_list = self.data_handler.get_current_map_characters_list()
        info = "현재 맵에 있는 캐릭터 목록:\n"
        for character_name in character_list:
            try:
                character = self.data_handler.get_character(character_name)
                info += f"이름: {character.name}\n"
                info += f"게임 속 역할: {character.type}\n"
                info += f"{character.get_info()}\n\n"
            except:
                print(f"캐릭터 {character_name}을 찾을 수 없습니다.")
        return info

    def get_characters_prior_messages(self):
        messages = []
        for character_name in self.get_npc_and_pokemon_list():
            character = self.data_handler.get_character(character_name)
            for message in character.chat_history:

                if message not in messages and message not in self.chat_history:
                    messages.append(message)
        return messages
    
    def recommend_user_chat(self):
        messages = []
        messages += self.get_characters_prior_messages()
        messages += self.chat_history
        messages += [self.make_message(role="user", content=RECOMMEND_USER_CHAT_PROMPT.format(
            current_map_name = self.data_handler.get_current_map().name,
            current_map_info = self.data_handler.get_current_map().info,
            character_info = self.get_characters_info(),
        ))]
        if self.provider == "openai":
            chat = self.get_response_structured_output(messages, manager_format.RecommendUserChat).chat
        elif self.provider == "anthropic":
            chat = self.get_response_function_calling(messages, manager_tools.recommend_user_chat(self.provider)).input['chat']
        elif self.provider == "google":
            chat = self.get_response_function_calling(messages, manager_tools.recommend_user_chat(self.provider)).args['chat']
        return chat

    def choose_action(self, message_list, talk_target=None):
        if len(message_list) > 0:
            self.add_messages_in_range(message_list)
            for message in message_list:
                self.add_message(message)

        messages = []
        messages += [self.make_message(role="user", content=CHOOSE_ACTION_PROMPT.format(
            current_map_name = self.data_handler.get_current_map().name,
            current_map_info = self.data_handler.get_current_map().info,
            character_info = self.get_characters_info(),
        ))] 
        messages += self.get_characters_prior_messages()
        messages += self.chat_history
        if self.provider in ["openai"]:
            action = self.get_response_structured_output(messages, manager_format.choose_action(
                character_list = self.get_npc_and_pokemon_list(),
            )).action
            print(action)
            if action.type=="choose_character":
                action = {
                    "type": "choose_character",
                    "name": action.name
                }
                type = self.data_handler.get_type_by_name(action['name'])
                if type == "npc":
                    output = self.npc_action(action)
                elif type == "pokemon":
                    output = self.pokemon_action(action)
                return output
            else:
                action = {
                    "type": "end_action"
                }
                return action
        elif self.provider in ["anthropic", "google"]:
            action = self.get_response_function_calling(messages, manager_tools.choose_action(
                character_list = self.get_npc_and_pokemon_list(),
                provider = self.provider,
                talk_target = talk_target
            ))
            print(action)
            if action.name=="choose_character":
                if self.provider == "anthropic":
                    action = {
                        "type": "choose_character",
                        "name": action.input['name']
                    }
                elif self.provider == "google":
                    action = {
                        "type": "choose_character",
                        "name": action.args['name']
                    }
                type = self.data_handler.get_type_by_name(action["name"])
                if type == "npc":
                    output = self.npc_action(action)
                elif type == "pokemon":
                    output = self.pokemon_action(action)
                return output
            else:
                action = {
                    "type": "end_action"
                }
                return action
    
    def npc_action(self, action):
        npc = self.data_handler.npc.get_npc(action['name'])
        npc_agent = NPCAgent(npc, self.data_handler)
        action = npc_agent.choose_action()
        if action['type'] == "speak":
            print(f"type={action['type']} name={action['name']} target={action['target']}")
            npc_name = action['name']
            target_name = action['target']
            chat = action['chat']
            message = self.make_message(role="assistant", content=f"{npc_name}->{target_name}: {chat}")
            self.add_messages_in_range([message])
            self.add_message(message)
        elif action['type'] == "give_pokemon":
            print(f"type={action['type']} name={action['name']} target={action['target']} pokemon={action['pokemon']}")
            pokemon_name = action['pokemon']
            npc_name = action['name']
            target_name = action['target']
            chat = action['chat']
            message1 = self.make_message(role="assistant", content=f"{npc_name}->{target_name}: {chat}")
            npc_name = josa(npc_name, "이")
            pokemon_name = josa(pokemon_name, "을")
            message2 = self.make_message(role="assistant", content=f"시스템: {npc_name} {target_name}에게 {pokemon_name} 주었습니다.")
            self.add_messages_in_range([
                message1, 
                message2
            ])
            self.add_message(message1)
            self.add_message(message2)
        elif action['type'] == "give_item":
            print(f"type={action['type']} name={action['name']} target={action['target']} item={action['item']} num={action['num']}")
            chat = action['chat']
            target_name = action['target']
            npc_name = action['name']
            item_name = action['item']
            message1 = self.make_message("assistant", f"{npc_name}->{target_name}: {chat}")
            npc_name = josa(npc_name, "이")
            item_name = josa(item_name, "을")
            message2 = self.make_message("assistant", f"시스템: {npc_name} {target_name}에게 {item_name} {action['num']}개 주었습니다.")
            self.add_messages_in_range([
                message1, 
                message2
            ])
            self.add_message(message1)
            self.add_message(message2)
        elif action['type'] == "call_character":
            print(f"type={action['type']} name={action['name']} target={action['target']}")
            chat = action['chat']
            target_name = action['target']
            npc_name = action['name']
            message = self.make_message("assistant", f"{npc_name}->{target_name}: {chat}")
            self.add_messages_in_range([message])
            self.add_message(message)
        elif action['type'] == "move_map":
            print(f"type={action['type']} name={action['name']} map={action['map']} spot={action['spot']}")
            map_name = action['map']
            npc_name = action['name']
            spot_name = action['spot']
            behavior = action['behavior']
            message = self.make_message("assistant", f"시스템: {npc_name}이 {map_name}-{spot_name}으로 이동했습니다.")
            message_behavior = self.make_message("assistant", f"시스템: ({npc_name}의 행동) {behavior}")
            self.add_messages_in_range([message])
            self.add_messages_in_range([message, message_behavior], map_name=map_name)
            self.add_message(message)
            self.add_message(message_behavior)
        elif action['type'] == "move_spot":
            print(f"type={action['type']} name={action['name']} spot={action['spot']}")
            spot_name = action['spot']
            npc_name = action['name']
            behavior = action['behavior']
            message = self.make_message("assistant", f"시스템: {npc_name}이 {spot_name}으로 이동했습니다.")
            message_behavior = self.make_message("assistant", f"시스템: ({npc_name}의 행동) {behavior}")
            self.add_messages_in_range([message, message_behavior])
            self.add_message(message)
            self.add_message(message_behavior)
        elif action['type'] == "initiate_battle":
            print(f"type={action['type']} name={action['name']} target={action['target']}")
            chat = action['chat']
            target_name = action['target']
            npc_name = action['name']
            message1 = self.make_message("assistant", f"{npc_name}->{target_name}: {chat}")
            message2 = self.make_message("assistant", f"시스템: {npc_name}이 {target_name}에게 승부를 걸었다.")
            self.add_messages_in_range([message1, message2])
            self.add_message(message1)
            self.add_message(message2)

        return action

    def pokemon_action(self, action):
        pokemon = self.data_handler.pokemon.get_pokemon(action['name'])
        pokemon_agent = PokemonAgent(pokemon, self.data_handler)
        action = pokemon_agent.speak()
        pokemon_name = action['name']
        target_name = action['target']
        message = self.make_message(role="assistant", content=f"{pokemon_name}: {action['chat']}")
        self.add_messages_in_range([message])
        self.add_message(message)
        return action