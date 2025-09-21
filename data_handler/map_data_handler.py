from .basic_data_handler import BasicDataHandler

class MapDataHandler(BasicDataHandler):
    def __init__(self, data):
        super().__init__(data)
    
    def get_map(self, map_name):
        return self.data[map_name]
    
    def get_map_list(self):
        return list(self.data.keys())

    def get_spots(self, map_name):
        map = self.get_map(map_name)
        return map.spots
    
    def get_spot(self, map_name, spot_name):
        spots = self.get_spots(map_name)
        return spots[spot_name]
    
    def get_characters(self, map_name):
        map = self.get_map(map_name)
        return map.characters
    
    def get_connected_maps(self, map_name):
        map = self.get_map(map_name)
        return map.connected_maps
    
    def remove_character_from_map(self, character):
        map = self.get_map(character.map)
        del map.characters[character.name]

    def add_character_from_map(self, character, map_name, position):
        map = self.get_map(map_name)
        map.characters[character.name] = {
            "type": character.type,
            "x": position[0],
            "y": position[1]
        }
            
    def move_character(self, character, map_name, position):
        self.remove_character_from_map(character)
        self.add_character_from_map(character, map_name, position)
    
    def get_position(self, map_name, target_name):
        map = self.get_map(map_name)
        # target이 캐릭터인지 spot인지 확인
        if target_name in map.characters:
            target = map.characters[target_name]
        else:
            target = map.spots[target_name]
        return [target['x'], target['y']]

    