from entity import Pokemon, Item

class UserAction:
    def __init__(self, user_action):
        self.action = user_action.action
        self.chat = user_action.chat
        self.item = Item(user_action.itemId)
        self.pokemon = Pokemon(user_action.pokemon)
        

class User:
    def __init__(self, user_info):
        self.name = user_info.name
        self.sex = user_info.sex
        self.first_pokemon = Pokemon(user_info.firstPoke)
