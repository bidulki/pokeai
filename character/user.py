class User:
    def __init__(self):
        self.type = "user"

    def set_from_data(self, user_data):
        self.name = user_data['name']
        self.sex = user_data['sex']
        self.map = user_data['map']
        self.money = user_data['money']
        self.pokemon_list = user_data['pokemon_list']
        self.inventory = user_data['inventory']

    def set_default(self):
        self.name = "레드"
        self.sex = "남성"
        self.map = "레드의집 2층"
        self.money = 3000
        self.pokemon_list = []
        self.inventory = [["상처약", 1]]
    
    def get_pokemon_info(self):
        pokemon_info = f"{self.name}의 지닌 포켓몬 목록:\n"
        if len(self.pokemon_list) == 0:
            return f"{self.name}은 포켓몬을 소유하고 있지 않습니다."
        else:
            pokemon_info += ", ".join(self.pokemon_list)
        return pokemon_info

    def get_info(self):
        info = f"태초마을에서 태어난 11세 소년, 그린과는 소꿉친구이다.\n"
        info += f"{self.get_pokemon_info()}\n"
        return info
    
    def get_item_num(self, item_name):
        for item in self.inventory:
            if item[0] == item_name:
                return item[1]
        return 0
    
    def add_item(self, item_name, num):
        if self.get_item_num(item_name) == 0:
            self.inventory.append([item_name, num])
        else:
            for item in self.inventory:
                if item[0] == item_name:
                    item[1] += num
                    break
        return
    
    def remove_item(self, item_name, num):
        for item in self.inventory:
            if item[0] == item_name:
                item[1] -= num
                if item[1] <= 0:
                    self.inventory.remove(item)
                break
        return
    
    def change_pokemon_order(self, pokemon_name_1, pokemon_name_2):
        pokemon_index_1 = self.pokemon_list.index(pokemon_name_1)
        pokemon_index_2 = self.pokemon_list.index(pokemon_name_2)
        self.pokemon_list[pokemon_index_1], self.pokemon_list[pokemon_index_2] = self.pokemon_list[pokemon_index_2], self.pokemon_list[pokemon_index_1]
        return
    
    def to_json(self):
        user_data = {
            "name": self.name,
            "sex": self.sex,
            "map": self.map,
            "money": self.money,
            "pokemon_list": self.pokemon_list,
            "inventory": self.inventory
        }
        return user_data