import sys
sys.path.append("/home/bidulki/develop/pokeai")
from entity import NPC, Pokemon, Location
from model import *
import requests
import os

class Client:
    def __init__(self):
        self.user = UserInfo(name="레드", sex="male")
        self.location = Location(1)
        self.user_pokemon_list = []
        self.items = []
        self.url = "http://127.0.0.1:8000"
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
    
    def send_request(self, api, param):
        url = os.path.join(self.url, api)
        response = requests.post(url, json=param)
        res = response.json()
        return res

    def choose_action(self):
        print("어떤 행동을 하겠습니까?")
        print("1. 대화한다 2. 배틀한다 3. 건네준다 4. 포획한다 5. 그만둔다")

        action_dict = {
            "1": "chat",
            "2": "battle",
            "3": "give",
            "4": "catch",
            "5": "quit"
        }
        
        action_num = int[input("번호 입력: ")]
        action = action_dict[action_num]
        if action=="chat":
            chat = input(f"{self.user.name}: ")
            user_action = UserAction(action=action, chat=chat)
        elif action=="give":
            if len(self.items) == 0:
                print("건네줄 물건이 없다!")
                return self.choose_action()
            print("어떤 물건을 건네줄 것인가?")
            for i, item in enumerate(self.items):
                print(f"{i}: {item.name}")

            itemId = 1
            user_action = UserAction(action=action, itemId=itemId)
        elif action=="catch":
            print("몬스터볼을 던졌다.")
            user_action = UserAction(action=action)
        else:
            user_action = UserAction(action=action)
        
        return user_action

    def talk_with_pokemon(self, pokemon):
        user_action = self.choose_action()

    def talk_with_npc(self, npc):
        user_action = self.choose_action()

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
        
        select_num = int(input("번호 입력: "))
        select = select_dict[select_num]

        print("-----------------------------------------------------------------------")
        print(f"{select.name}과 대화를 시작합니다.")

        if isinstance(select, NPC):
            self.talk_with_npc(select)
        else:
            self.talk_with_pokemon(select)

    def start(self):
        print(f"현재위치: {self.location.name}")
        print(f"당신의 이름은 {self.user.name}, 오박사에게 포켓몬을 받으러 오박사 연구소에 왔다.")
        print("-----------------------------------------------------------------------")
        self.select_to_talk()

if __name__=="__main__":
    client = Client()
    client.start()