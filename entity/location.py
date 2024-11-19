import json
import os

class Location:
    def __init__(self, location_id):
        self.id = location_id
        self.load_location_info(location_id)
    
    def load_location_info(self, location_id):
        location_file_path = os.path.join("./locations", f"{location_id}.json")
        with open(location_file_path, 'r') as f:
            location_json = json.load(f)
        
        self.name = location_json['name']
        self.description = "\n".join(location_json['description'])