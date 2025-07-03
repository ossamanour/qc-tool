"""
Class for advanced configure file.
"""
import os
import json


class AdvancedConfigJson():
    """
    Class for advanced config file
    """
    def __init__(self, config_path=None):
        self.config_path = config_path
        if os.path.exists(self.config_path):
            with open(config_path) as f:
                self.config_json = json.load(f)
        else:
            self.config_json = {}
            self.save()

    def save(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config_json, f, indent=4)

    def update_item(self, category, key, value):
        if category not in self.config_json:
            self.config_json[category] = {}
        self.config_json[category][key] = value
        self.save()

    def update_dict(self, dict):
        for category in dict.keys():
            print(category)
            if category not in self.config_json:
                self.config_json[category] = {}
            for key in dict[category].keys():
                self.config_json[category][key] = dict[category][key]
        self.save()

    def load(self, category, key):
        if category in self.config_json:
            if key in self.config_json[category]:
                return self.config_json[category][key]
        
        return None
    
    def check(self, category, key):
        if category in self.config_json:
            if key in self.config_json[category] and self.config_json[category][key] != None:
                return True
        else:
            return False