class NPC:
    def __init__(self, npc_data):
        self.type = "npc"
        self.name = npc_data['name']
        self.info = npc_data['info']
        self.map = npc_data['map']
        self.pokemon_list = npc_data['pokemon_list']
        self.inventory = npc_data['inventory']
        self.chat_history = npc_data['chat_history']
        
    def get_item_list(self):
        item_list = []
        for item in self.inventory:
            item_list.append(item[0])
        return item_list
    
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

    def get_pokemon_info(self):
        pokemon_info = f"{self.name}의 지닌 포켓몬 목록:\n"
        if len(self.pokemon_list) == 0:
            return f"{self.name}은 포켓몬을 소유하고 있지 않습니다."
        else:
            pokemon_info += ", ".join(self.pokemon_list)
        return pokemon_info
    
    def get_item_info(self):
        item_info = f"{self.name}의 지닌 아이템 목록:\n"
        if len(self.inventory) == 0:
            return f"{self.name}은 아이템을 소유하고 있지 않습니다."
        else:
            for item in self.inventory:
                item_info += f"{item[0]}: {item[1]}개\n"
        return item_info
    
    def get_info(self):
        npc_info = f"정보: {' '.join(self.info)}\n"
        npc_info += f"{self.get_pokemon_info()}\n"
        npc_info += f"{self.get_item_info()}\n"
        return npc_info

    def to_json(self):
        npc_data = {
            "name": self.name,
            "info": self.info,
            "map": self.map,
            "pokemon_list": self.pokemon_list,
            "inventory": self.inventory,
            "chat_history": self.chat_history
        }
        return npc_data
        