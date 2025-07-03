"""
Class for project configuration.
"""
import os
import json


class ProjectConfigJson():
    """
    Class for project config file
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

    def update(self, key, value):
        self.config_json[key] = value
        self.save()

    def load(self, key):
        if key in self.config_json:
            return self.config_json[key]
        
        return None

    def check(self, key):
        if key in self.config_json and self.config_json[key] != None:
            return True
        else:
            return False