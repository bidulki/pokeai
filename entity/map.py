class Map:
    def __init__(self, map_data):
        self.name = map_data['name']
        self.info = map_data['info']
        self.width = map_data['width']
        self.height = map_data['height']
        self.characters = map_data['characters']
        self.connected_maps = map_data['connected_maps']
        self.spots = map_data['spots']

    def to_json(self):
        map_data = {
            "name": self.name,
            "info": self.info,
            "width": self.width,
            "height": self.height,
            "characters": self.characters,
            "connected_maps": self.connected_maps,
            "spots": self.spots
        }
        return map_data