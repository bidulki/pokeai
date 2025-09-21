from .basic_data_handler import BasicDataHandler

class NPCDataHandler(BasicDataHandler):
    def __init__(self, data):
        super().__init__(data)

    def get_npc(self, name):
        return self.data[name]
    
    def get_info(self, name):
        npc = self.get_npc(name)
        return npc.info

    def get_map(self, name):
        npc = self.get_npc(name)
        return npc.map 
    
    def get_pokemon_list(self, name):
        npc = self.get_npc(name)
        return npc.pokemon_list
    
    def add_message(self, name, message):
        npc = self.get_npc(name)
        npc.chat_history.append(message)

    def add_messages(self, name, message_list):
        npc = self.get_npc(name)
        for message in message_list:
            npc.chat_history.append(message)

    def get_chat_history(self, name):
        npc = self.get_npc(name)
        return npc.chat_history 