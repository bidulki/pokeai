class BasicDataHandler:
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data
    
    def get_keys(self):
        return list(self.data.keys())