import sys
sys.path.append("../")

from agent import AgentManager
from data_manager import DataManager
from data_handler import DataHandler
from utils import *

class Game:
    """포켓몬 게임의 메인 클래스로 게임 진행과 사용자 상호작용을 관리합니다."""

    def __init__(self, savedata_dir, data):
        """게임 초기화 함수
        
        Args:
            savedata_dir (str): 세이브 데이터 디렉토리 경로
            data (dict): 게임 데이터
        """
        self.savedata_dir = savedata_dir
        self.data_handler = DataHandler(data)
        self.agent_manager = AgentManager(savedata_dir, self.data_handler)
        self.user_name = self.data_handler.user.get_name()

    def run(self):
        """게임 메인 루프를 실행합니다."""
        while True:
            self.user_action()

    def user_action(self):
        """사용자 액션 메뉴를 표시하고 선택된 액션을 실행합니다."""

        options = {
            "1": ("물건 조사", self.inspect_spot),
            "2": ("말걸기", self.talk),
            "3": ("이동", self.user_move),
            "4": ("가방", self.check_inventory),
            "5": ("포켓몬", self.check_pokemon),
            "6": ("리포트", self.save),
            "7": ("게임종료", self.end)
        }

        print("무엇을 하시겠습니가?")
        for key, (name, _) in options.items():
            print(f"{key}: {name}")

        select = input("선택: ")
        input(">>")

        if select in options:
            options[select][1]()
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")
            self.user_action()
    
    def process_user_input(self):
        user_input = get_user_input()
        if user_input == "q":
            message = {"role": "user", "content": f"시스템: 대화가 종료되었다."}
            self.agent_manager.add_messages_in_range([message])
            self.agent_manager.add_message(message)
            return False
        elif user_input == "!추천":
            chat = self.agent_manager.recommend_user_chat()
            print_and_wait(chat)
            self.process_user_input()
        elif user_input != "":
            message = {"role": "user", "content": f"{self.user_name}: {user_input}"}
            self.call_agent_manager([message])
            return True
        else:
            self.call_agent_manager()
            return True
    
    def call_agent_manager(self, message_list=None, target=None):
        if message_list is None:
            message_list = []

        action = self.agent_manager.choose_action(message_list, target)

        if action['type'] == "speak":
            self._handle_speak_action(action)
        elif action['type'] == "give_pokemon":
            self._handle_give_pokemon_action(action)
        elif action['type'] == "give_item":
            self._handle_give_item_action(action)
        elif action['type'] == "call_character":
            self._handle_call_character_action(action)
        elif action['type'] == "move_map":
            self._handle_move_map_action(action)
        elif action['type'] == "move_spot":
            self._handle_move_spot_action(action)
    
    def _handle_speak_action(self, action):
        """말걸기 액션을 처리합니다.
        
        Args:
            action: 에이전트로부터 받은 출력 객체
        """
        name = josa(action['name'], "이")
        print(f"{name} {action['target']}에게 말을 걸었다.")
        print(f"{action['chat']}")
        self.process_user_input()
    
    def _handle_give_pokemon_action(self, action):
        """포켓몬 주기 액션을 처리합니다.
        
        Args:
            action: 에이전트로부터 받은 출력 객체
        """
        pokemon_name = action['pokemon']
        npc_name = action['name']
        target_name = action['target']

        # 포켓몬 이름 처리
        pokemon_name_with_josa = pokemon_name.split("_")[0]
        pokemon_name_with_josa = josa(pokemon_name_with_josa, "을")

        print_and_wait(f"{action['chat']}")

        # 플레이어에게 포켓몬 주기
        if target_name == self.user_name:
            choice = select_yes_or_no(f"{npc_name}에게 {pokemon_name_with_josa} 받겠습니까?")
            if choice != "1":
                message = {"role": "user", "content": f"시스템: {npc_name}에게 {pokemon_name_with_josa} 받기를 거절했다."}
                self.agent_manager.add_messages_in_range([message])
                self.agent_manager.add_message(message)
                self.process_user_input()
                return
            else:
                pokemon = self.data_handler.pokemon.get_pokemon(pokemon_name)
                self.data_handler.pokedex.catch_pokemon(pokemon.pokedex)
        self.data_handler.give_pokemon(pokemon_name, npc_name, target_name)
        if target_name == self.user_name:
            print(f"{npc_name}에게 {pokemon_name_with_josa} 받았다!")
        else:
            npc_name_with_josa = josa(npc_name, "이")
            print(f"{npc_name_with_josa} {target_name}에게 {pokemon_name_with_josa} 주었다.")
        
        self.process_user_input()
    
    def _handle_give_item_action(self, action):
        """아이템 주기 액션을 처리합니다.
        
        Args:
            action: 에이전트로부터 받은 출력 객체
        """
        item_name = action['item']
        npc_name = action['name']
        target_name = action['target']
        num = action['num']
        
        print_and_wait(f"{action['chat']}")

        # 플레이어에게 아이템을 줄 경우 확인
        if target_name == self.user_name:
            choice = select_yes_or_no(f"{npc_name}에게 {item_name} {num}개를 받겠습니까?")
            if choice != "1":
                message = {"role": "user", "content": f"시스템: {npc_name}에게 {item_name} {num}개를 받기를 거절했다."}
                self.agent_manager.add_messages_in_range([message])
                self.agent_manager.add_message(message)
                self.process_user_input()
                return
        
        self.data_handler.give_item(item_name, npc_name, target_name, num)
            
        item_name_with_josa = josa(item_name, "을")
        if target_name == self.user_name:
            print(f"{npc_name}에게 {item_name_with_josa} {num}개 받았다.")
        else:
            npc_name_with_josa = josa(npc_name, "이")
            print(f"{npc_name_with_josa} {target_name}에게 {item_name_with_josa} {num}개 주었다.")
            
        self.process_user_input()
    
    def _handle_call_character_action(self, action):
        """캐릭터 불러오기 액션을 처리합니다.
        
        Args:
            action: 에이전트로부터 받은 출력 객체
        """
        npc_name = action['name']
        target_name = action['target']

        # target을 npc 앞으로 이동
        map_name = self.data_handler.get_current_map().name
        self.data_handler.character_move_spot(target_name, map_name, npc_name)
        npc_name_with_josa = josa(action['name'], "이")
        print(f"{npc_name_with_josa} {action['target']}를 불렀다.")
        print(f"{action['chat']}")
        target_name_with_josa = josa(target_name, "이")
        message = {"role": "user", "content": f"시스템: {target_name_with_josa} {npc_name}에게 다가왔다."}
        self.call_agent_manager([message], npc_name)

    def _handle_move_map_action(self, action):
        """맵 이동 액션을 처리합니다.
        
        Args:
            action: 에이전트로부터 받은 출력 객체
        """
        npc_name = action['name']
        map_name = action['map']
        spot_name = action['spot']

        npc_name_with_josa = josa(npc_name, "이")
        print(f"{npc_name_with_josa} {map_name}으로 이동했다.")
        self.data_handler.character_move_map(npc_name, map_name, spot_name)
        self.call_agent_manager()

    def _handle_move_spot_action(self, action):
        """지점 이동 액션을 처리합니다.
        
        Args:
            action: 에이전트로부터 받은 출력 객체
        """
        npc_name = action['name']
        spot_name = action['spot']
        current_map = self.data_handler.get_current_map()
        map_name = current_map.name
        npc_name_with_josa = josa(npc_name, "이")
        print(f"{npc_name_with_josa} {spot_name}으로 이동했다.")
        self.data_handler.character_move_spot(npc_name, map_name, spot_name)
        self.call_agent_manager([], npc_name)

    def inspect_spot(self):
        """현재 맵의 특정 지점을 조사합니다."""
        print("무엇을 조사할까요?")

        current_map = self.data_handler.get_current_map()
        current_spots = self.data_handler.get_current_spots()
        current_spots_list = list(current_spots.keys())

        inspect_target = select_item_from_list(current_spots_list)
        if not inspect_target:
            return
        
        # 선택한 지점으로 이동
        self.data_handler.user_move_spot(inspect_target)

         # 시스템 메시지 생성
        content = f"시스템: 레드가 {inspect_target}을 조사했다."
        spot_data = current_map.spots[inspect_target]

        # 조사 메시지 출력 및 메시지 리스트 생성
        message_list = [{"role": "user", "content": content}]
        for message in spot_data['inspect']:
            print_and_wait(message)
            content += "\n" + message
        
        # 에이전트 호출
        self.call_agent_manager(message_list)
    
    def talk(self):
        """현재 맵의 특정 캐릭터에게 말을 겁니다."""
        print("누구에게 말을 걸까요?")

        # 현재 맵의 캐릭터 목록 가져오기
        current_characters = self.data_handler.get_current_map_characters()
        current_characters_list = list(current_characters.keys())

        # 사용자 이름 제외
        current_characters_list.remove(self.user_name)

        # 대화 대상 선택
        talk_target = select_item_from_list(current_characters_list)
        if not talk_target:
            return 
        
        # 선택한 캐릭터 위치로 이동
        character = current_characters[talk_target]
        position = [character['x'], character['y']]
        self.data_handler.user_move_position(position)

        if character['type'] == "npc":
            self._talk_to_npc(talk_target)
        elif character['type'] == "pokemon":
            self._talk_to_pokemon(talk_target)
    
    def _talk_to_npc(self, talk_target):
        message = {"role": "user", "content": f"레드가 {talk_target}에게 말을 걸었다."}
        self.call_agent_manager([message], talk_target)

    def _talk_to_pokemon(self, talk_target):
        pokemon = self.data_handler.pokemon.get_pokemon(talk_target)
        self.data_handler.pokedex.meet_pokemon(pokemon.pokedex)
        print_and_wait("무엇을 하시겠습니까?")
        options = ["말걸기", "포켓몬 도감 확인"]
        action = select_item_from_list(options)
        if not action:
            return
        
        if action == "말걸기":
            message = {"role": "user", "content": f"시스템: 레드가 {talk_target}에게 말을 걸었다."}
            self.call_agent_manager([message], talk_target)
        elif action == "포켓몬 도감 확인":
            self.check_pokedex(pokemon.pokedex)
    
    def check_pokedex(self, pokedex):
        # 도감 정보 가져오기
        pokedex_data = self.data_handler.pokedex.get_pokedex(pokedex)
        name = pokedex_data['name']
        category = pokedex_data['category']
        types = pokedex_data['type']
        description = pokedex_data['description']
        print(f"{name} - {category}")
        print(f"{', '.join(types)} 타입")
        print_and_wait(f"{description}")
    
    def user_move(self):
        """다른 맵으로 이동합니다."""
        print("어디로 이동할까요?")

        # 현재 연결된 맵 목록 가져오기
        current_connected_maps = self.data_handler.get_current_connected_maps()
        current_connected_maps_list = list(current_connected_maps.keys())

        # 이동할 맵 선택
        target_map = select_item_from_list(current_connected_maps_list)
        if not target_map:
                return
        
        # 이동 메시지 생성 및 전파
        message = f"레드가 {target_map}으로 이동합니다."
        self.agent_manager.add_messages_in_range([{"role": "user", "content": message}])
        print_and_wait(message)

        # 맵 이동 처리
        self.data_handler.user_move_map(target_map)

        # 에이전트 호출
        self.call_agent_manager([{"role": "user", "content": message}])

    def check_inventory(self):
        """인벤토리를 확인하고 아이템 정보를 표시합니다."""

        # 유저 돈 표시
        user_money = self.data_handler.user.get_money()
        print_and_wait(f"용돈: {user_money}")

        # 인벤토리 아이템 선택 및 정보 표시
        user_inventory = self.data_handler.user.get_inventory()
        item_selected_name = select_item_from_inventory(user_inventory)
        if item_selected_name:
            item_selected_info = self.data_handler.item.get_info(item_selected_name)
            print_and_wait(item_selected_info)
    
    def check_pokemon(self):
        """보유한 포켓몬 목록을 확인하고 상세 정보를 표시합니다."""
        user_pokemon_list = self.data_handler.user.get_pokemon_list()
        
        if not user_pokemon_list:
            print_and_wait("현재 소유한 포켓몬이 없습니다.")
            return
        
        print("소유한 포켓몬 목록:")
        selected_pokemon_name = select_item_from_list(user_pokemon_list)
        
        if not selected_pokemon_name:
            return
        
        action_options = ["능력치를 본다", "순서바꾸기"]
        selected_action = select_item_from_list(action_options)

        if not selected_action:
            return
        
        if selected_action == "능력치를 본다":
            # 선택한 포켓몬의 상세 정보 표시
            pokemon = self.data_handler.pokemon.get_pokemon(selected_pokemon_name)
            self._display_pokemon_details(pokemon)
        elif selected_action == "순서바꾸기":
            # 포켓몬 순서 변경
            self._change_pokemon_order(selected_pokemon_name, user_pokemon_list)
        self.check_pokemon()
    
    def _display_pokemon_details(self, pokemon):
        """포켓몬의 상세 정보를 표시합니다."""
        print_and_wait("\n===== 포켓몬 상세 정보 =====")
        pokemon_name = pokemon.name.split("_")[0]
        print(f"이름: {pokemon_name}")
        print(f"레벨: {pokemon.level}")
        print(f"타입: {', '.join(pokemon.types)}")
        print(f"HP: {pokemon.hp}/{pokemon.stats['HP']}")
        print(f"상태: {pokemon.status}")

        # 도감 정보
        print_and_wait("\n----- 도감 정보 -----")
        print(f"종류: {pokemon.pokedex}")
        print(f"도감번호: {pokemon.id}")
        print(f"도감설명: {pokemon.description}")
        print(f"분류: {pokemon.category}")
        print(f"키: {pokemon.height}m")
        print(f"몸무게: {pokemon.weight}kg")

        # 스탯 표시
        print_and_wait("\n----- 능력치 -----")
        print(f"공격: {pokemon.stats['Attack']}")
        print(f"방어: {pokemon.stats['Defense']}")
        print(f"특수공격: {pokemon.stats['Special Attack']}")
        print(f"특수방어: {pokemon.stats['Special Defense']}")
        print(f"스피드: {pokemon.stats['Speed']}")

        # 기술 표시
        print_and_wait("\n----- 기술 -----")
        for move in pokemon.moves:
            print(f"{move.name} - {move.type} 타입 / 위력: {move.power}")
            print(f"설명: {move.description}")

        # 경험치 표시
        print_and_wait("\n----- 경험치 -----")
        print(f"\n경험치: {pokemon.exp}/{pokemon.max_exp}")
        print_and_wait()

    def _change_pokemon_order(self, selected_pokemon_name, user_pokemon_list):
        """포켓몬 순서를 변경합니다."""
        print("변경할 포켓몬을 선택하세요.")
        selected_pokemon_name2 = select_item_from_list(user_pokemon_list)

        if not selected_pokemon_name2:
            return
        
        user = self.data_handler.user.get_data()
        user.change_pokemon_order(selected_pokemon_name, selected_pokemon_name2)
        print_and_wait(f"{selected_pokemon_name}와 {selected_pokemon_name2}의 순서를 변경했습니다.")

    def save(self):
        """게임 진행 상황을 저장합니다."""

        select = input("지금까지의 활약을 리포트로 작성할까요?\n1. 예 2. 아니오\n선택: ")
        input(">>")

        if select == "1": 
            self._save_game_data()
        elif select == "2":
            pass
        else:
            self.save()
    
    def _save_game_data(self):
        DataManager.save(self.savedata_dir, self.data_handler.get_data())
        self.agent_manager.save_log()
        print_and_wait("레드는 리포트를 꼼꼼히 작성했다!")
    
    def end(self):
        print("게임을 종료합니다.")
        sys.exit()