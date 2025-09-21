from .basic_data_handler import BasicDataHandler

class ItemDataHandler(BasicDataHandler):
    def __init__(self, data):
        super().__init__(data)
    
    def get_item(self, name):
        return self.data[name]
    
    def get_info(self, name):
        return self.data[name].info