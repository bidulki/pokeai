from .pokemon import Pokemon
from .item import Item

class UserAction:
    def __init__(self, user_action):
        self.action = user_action.action
        if user_action.chat==None:
            self.chat = None
        else:
            self.chat = user_action.chat

        if user_action.itemId==None:
            self.item = None
        else:
            self.item = Item(user_action.itemId)

        if user_action.pokemon==None:
            self.pokemon = None
        else:
            self.pokemon = Pokemon(user_action.pokemon)
        

class User:
    def __init__(self, user_info):
        self.name = user_info.name
        self.sex = user_info.sex
        if user_info.firstPoke == None:
            self.first_pokemon = None
        else:
            self.first_pokemon = Pokemon(user_info.firstPoke)
