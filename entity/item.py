class Item:
    def __init__(self, item_data):
        self.name = item_data['name']
        self.info = item_data['info']

class Ball(Item):
    def __init__(self, ball_data):
        super().__init__(ball_data)
        self.type = "ball"
        self.rate = ball_data['rate']
        self.price = ball_data['price']

class Stone(Item):
    def __init__(self, stone_data):
        super().__init__(stone_data)
        self.type = "stone"
        self.target = stone_data['target']
        self.price = stone_data['price']
    
class Restore(Item):
    def __init__(self, restore_data):
        super().__init__(restore_data)
        self.type = "restore"
        self.restore = restore_data['restore']
        self.recover = restore_data['recover']
        self.price = restore_data['price']

class Special(Item):
    def __init__(self, special_data):
        super().__init__(special_data)
        self.type = "special"
