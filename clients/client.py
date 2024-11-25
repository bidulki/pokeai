import sys
sys.path.append("../pokeai")
from entity import NPC, Pokemon, Location, Item
from model import *
import requests
import os

class Client:
    def __init__(self):
        self.url = "http://127.0.0.1:8000"
        self.user = UserInfo(name="레드", sex="male")
        self.location = Location(1)
        self.user_pokemon_list = []
        self.item_id_list = [1]
        self.NPC_id_list = [1]
        self.Pokemon_id_list = [
            {
                "id": 1,
                "dexNum": 1,
                "hp": 100,
                "status": "NOR"
            }, 
            {
                "id": 2,
                "dexNum": 4,
                "hp": 100,
                "status": "NOR"
            },
            {
                "id": 3,
                "dexNum": 7,
                "hp": 100,
                "status": "NOR"
            }
        ]
        self.load_npc()
        self.load_pokemon()
        self.load_item()
        self.NPC_chatHistory = {
            1: []
        }
        self.Pokemon_chatHistory = {
            1: [],
            2: [],
            3: []
        }
    
    def load_npc(self):
        self.NPC_list = []
        for npc_id in self.NPC_id_list:
            npc_info = NpcInfo(id=npc_id, pokeList=[])
            npc = NPC(npc_info)
            self.NPC_list.append(npc)
    
    def load_pokemon(self):
        self.Pokemon_list = []
        for poke in self.Pokemon_id_list:
            poke_info = PokeInfo(**poke)
            pokemon = Pokemon(poke_info)
            self.Pokemon_list.append(pokemon)
    
    def load_item(self):
        self.item_list = []
        for item_id in self.item_id_list:
            item = Item(item_id)
            self.item_list.append(item)
    
    def send_request(self, api, param):
        headers = {"Content-Type": "application/json"}
        url = os.path.join(self.url, api)
        response = requests.post(url, json=param.model_dump(), headers=headers)
        return response

    def make_message(self, role, content):
        message = {"role": role, "content": content}
        return message
    
    def choose_action(self, name):
        print("어떤 행동을 하겠습니까?")
        print("1. 대화한다 2. 배틀한다 3. 건네준다 4. 포획한다 5. 그만둔다")

        action_dict = {
            1: "chat",
            2: "battle",
            3: "give",
            4: "catch",
            5: "quit"
        }

        action_num = int(input("번호 입력: "))
        action = action_dict[action_num]
        if action=="chat":
            chat = input(f"{self.user.name}: ")
            user_action = UserAction(action=action, chat=chat)
            print("-----------------------------------------------------------------------")
        elif action=="battle":
            print(f"{name}에게 승부를 걸었다.")
            print("-----------------------------------------------------------------------")
            user_action = UserAction(action=action)
        elif action=="give":
            if len(self.item_list) == 0:
                print("건네줄 물건이 없다!")
                print("-----------------------------------------------------------------------")
                return self.choose_action(name)
            print(f"{name}에게 어떤 물건을 건네줄 것인가?")
            for i, item in enumerate(self.item_list):
                print(f"{i}: {item.name}")
            select_item_num = int(input("선택: "))
            select_item_id = self.item_list[select_item_num].id 
            user_action = UserAction(action=action, itemId=select_item_id)
        elif action=="catch":
            print(f"{name}에게 몬스터볼을 던졌다.")
            user_action = UserAction(action=action)
        elif action=="quit":
            print(f"{name}과의 대화를 종료했다.")
            user_action = UserAction(action=action)
        
        return user_action

    def talk_with_entity(self, entity, chatHistory):
        user_action = self.choose_action(entity.name)
        choices = []
        if user_action.action == "chat":
            conversation = Conversation(
                userInfo=self.user, 
                chatHistory=chatHistory, 
                userAction=user_action,
                locationId=self.location.id
            )
            if isinstance(entity, Pokemon):
                poke_info=dict(entity.poke_info)
                param = PokeChat(pokeInfo=poke_info, conversation=conversation)
                response = self.send_request("api/chat/poke", param)
                response = response.json()
                message = response.get("narration")
                chatHistory = response.get("chatHistory")
                self.Pokemon_chatHistory[entity.id] = chatHistory
            elif isinstance(entity, NPC):
                npc_info=dict(entity.npc_info)
                param = NpcChat(npcInfo=npc_info, conversation=conversation)
                response = self.send_request("api/chat/npc", param)
                response = response.json()
                message = response.get("message")
                choices = response.get("choices")
                chatHistory = response.get("chatHistory")
                self.NPC_chatHistory[entity.id] = chatHistory
                
            print(f"{message}")
            if len(choices)!=0:
                for i, choice in enumerate(choices):
                    print(f"{i+1}: {choice}")
            print("-----------------------------------------------------------------------")
            self.talk_with_entity(entity, chatHistory)
        elif user_action.action == "battle":
            print("구현 미완료")
            print("-----------------------------------------------------------------------")
            self.talk_with_entity(entity, chatHistory)
        elif user_action.action == "give":
            print("구현 미완료")
            print("-----------------------------------------------------------------------")
            self.talk_with_entity(entity, chatHistory)
        elif user_action.action == "catch":
            print("구현 미완료")
            print("-----------------------------------------------------------------------")
            self.talk_with_entity(entity, chatHistory)
        else:
            print("-----------------------------------------------------------------------")
            end_message = self.make_message("system", f"{self.user.name}이 대화를 그만두었다.")
            chatHistory.append(end_message)
            if isinstance(entity, Pokemon):
                self.Pokemon_chatHistory[entity.id].append(end_message)
            elif isinstance(entity, NPC):
                self.NPC_chatHistory[entity.id].append(end_message)
            self.select_to_talk()

    def select_to_talk(self):
        print("누구와 대화하겠습니까?")
        i = 0
        select_dict = {}
        for npc in self.NPC_list:
            print(f"{i}: {npc.name}")
            select_dict[i] = npc
            i+=1

        for pokemon in self.Pokemon_list:
            print(f"{i}: {pokemon.name}")
            select_dict[i] = pokemon
            i+=1
        
        print(f"{i}: 게임을 종료한다.")
        
        select_num = int(input("번호 입력: "))
        if select_num >= len(select_dict.keys()):
            return
        select = select_dict[select_num]

        print("-----------------------------------------------------------------------")
        print(f"{select.name}과 대화를 시작합니다.")
        user_action = UserAction(action="chat")
        choices=[]
        if isinstance(select, Pokemon):
            chatHistory = self.Pokemon_chatHistory[select.id]
            conversation = Conversation(
                userInfo=self.user,
                chatHistory=chatHistory,
                userAction=user_action,
                locationId=self.location.id
            )
            poke_info = dict(select.poke_info)
            param = PokeChat(pokeInfo=poke_info, conversation=conversation)
            response = self.send_request("api/chat/poke", param)
            response = response.json()
            chatHistory = response.get("chatHistory")
            self.Pokemon_chatHistory[select.id] = chatHistory
            
        else:
            chatHistory = self.NPC_chatHistory[select.id]
            conversation = Conversation(
                userInfo=self.user,
                chatHistory=chatHistory,
                userAction=user_action,
                locationId=self.location.id
            )
            npc_info=dict(select.npc_info)
            param = NpcChat(npcInfo=npc_info, conversation=conversation)
            response = self.send_request("api/chat/npc", param)
            response = response.json()
            message = response.get("message")
            choices = response.get("choices")
            chatHistory = response.get("chatHistory")
            self.Pokemon_chatHistory[select.id] = chatHistory
            
        print(f"{message}")
        if len(choices)!=0:
            for i, choice in enumerate(choices):
                print(f"{i+1}: {choice}")
        self.talk_with_entity(select, chatHistory)

    def start(self):
        print(f"당신의 이름은 {self.user.name}, 오박사에게 포켓몬을 받으러 오박사 연구소에 왔다.")
        print(f"현재위치: {self.location.name}")
        print(f"현재 인벤토리: ", end= "")
        for item in self.item_list:
            print(f"{item.name}", end=" ")
        print()
        print("-----------------------------------------------------------------------")
        self.select_to_talk()

if __name__=="__main__":
    client = Client()
    client.start()