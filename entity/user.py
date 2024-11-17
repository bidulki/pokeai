from pokemon import Pokemon

class User:
    def __init__(self, user_info):
        self.name = user_info.name
        self.sex = user_info.sex
        self.first_pokemon = Pokemon(user_info.firstPoke)
        