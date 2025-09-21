from .basic_data_handler import BasicDataHandler
from .map_data_handler import MapDataHandler
from .user_data_handler import UserDataHandler
from .item_data_handler import ItemDataHandler
from .npc_data_handler import NPCDataHandler
from .pokemon_data_handler import PokemonDataHandler
from .pokedex_data_handler import PokedexDataHandler

class DataHandler(BasicDataHandler):
    def __init__(self, data):
        super().__init__(data)
        self.map = MapDataHandler(data['map'])
        self.user = UserDataHandler(data['user'])
        self.item = ItemDataHandler(data['item'])
        self.npc = NPCDataHandler(data['npc'])
        self.pokemon = PokemonDataHandler(data['pokemon'])
        self.pokedex = PokedexDataHandler(data['pokedex'])  
    
    def get_current_map(self):
        user_map_name = self.user.get_map()
        current_map = self.map.get_map(user_map_name)
        return current_map
    
    def get_current_spots(self):
        user_map_name = self.user.get_map()
        current_spots = self.map.get_spots(user_map_name)
        return current_spots
    
    def get_current_connected_maps(self):
        user_map_name = self.user.get_map()
        current_connected_maps = self.map.get_connected_maps(user_map_name)
        return current_connected_maps
    
    def get_current_map_characters(self):
        user_map_name = self.user.get_map()
        current_map_characters = self.map.get_characters(user_map_name)
        return current_map_characters
    
    def get_current_map_characters_list(self):
        current_map_characters = self.get_current_map_characters()
        character_list = list(current_map_characters.keys())
        return character_list

    def user_move_map(self, target_map_name):
        current_connected_maps = self.get_current_connected_maps()
        target_map = current_connected_maps[target_map_name]
        target_position = [target_map['x'], target_map['y']]
        self.map.move_character(
            character=self.user.get_data(),
            map_name=target_map_name,
            position=target_position
        )
        self.user.set_map(target_map_name)

    def user_move_spot(self, spot_name):
        current_spots = self.get_current_spots()
        spot = current_spots[spot_name]
        position = [spot['x'], spot['y']]
        self.map.move_character(
            character=self.user.get_data(),
            map_name=self.user.get_map(),
            position=position
        )

    def user_move_position(self, position):
        self.map.move_character(
            character=self.user.get_data(),
            map_name=self.user.get_map(),
            position=position
        )
    
    def check_talkable(self, map_name, character_name, target_name, max_distance):
        character_position = self.map.get_position(map_name, character_name)
        target_position = self.map.get_position(map_name, target_name)
        # 택시 기하학 거리 계산
        distance = abs(character_position[0] - target_position[0])
        distance += abs(character_position[1] - target_position[1])
        if distance <= max_distance:
            return True
        else:
            return False

    
    def get_type_by_name(self, name):
        if name == self.user.get_name():
            return "user"
        elif name in self.npc.get_keys():
            return "npc"
        elif name in self.pokemon.get_keys():
            return "pokemon"
        elif name in self.map.get_keys():
            return "map"
        elif name in self.item.get_keys():
            return "item"
        else:
            return "spot"
    
    def get_character(self, character_name):
        type = self.get_type_by_name(character_name)
        if type == "user":
            character = self.user.get_data()
        elif type == "npc":
            character = self.npc.get_npc(character_name)
        elif type == "pokemon":
            character = self.pokemon.get_pokemon(character_name)
        else:
            character = None
        return character
    
    def character_move_spot(self, character_name, map_name, spot_name):
        # spot_name이 캐릭터의 이름이면 캐릭터의 위치로 이동
        character_list = list(self.map.get_characters(map_name).keys())
        if spot_name in character_list:
            spot = self.map.get_characters(map_name)[spot_name]
        else:
            spot = self.map.get_spot(map_name, spot_name)
        character = self.get_character(character_name)
        position = [spot['x'], spot['y']]
        self.map.move_character(
            character=character,
            map_name=map_name,
            position=position
        )
    
    def character_move_map(self, character_name, map_name, spot_name):
        self.character_move_spot(character_name, map_name, spot_name)
        character = self.get_character(character_name)
        character.map = map_name
    
    def give_pokemon(self, pokemon_name, master_name, target_name):
        pokemon = self.pokemon.get_pokemon(pokemon_name)
        master = self.get_character(master_name)
        target = self.get_character(target_name)
        master.pokemon_list.remove(pokemon_name)
        target.pokemon_list.append(pokemon_name)
        pokemon.master = target_name
        return

    def give_item(self, item_name, master_name, target_name, num):
        master = self.get_character(master_name)
        target = self.get_character(target_name)
        master.remove_item(item_name, num)
        target.add_item(item_name, num)
        return
    
    def add_message(self, character_name, message):
        type = self.get_type_by_name()
        if type=="npc":
            self.npc.add_message(character_name, message)
        else:
            self.pokemon.add_message(character_name, message)

    def add_messages(self, character_name, message_list):
        type = self.get_type_by_name()
        if type=="npc":
            self.npc.add_messages(character_name, message_list)
        else:
            self.pokemon.add_messages(character_name, message_list)



    
