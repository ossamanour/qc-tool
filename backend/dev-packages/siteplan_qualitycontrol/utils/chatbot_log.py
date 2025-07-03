"""
Class for ChatBot response.
"""
import os
import json


class ChatBotInputJson():
    """
    Class for ChatBot response
    """
    def __init__(self, log_path=None):
        self.log_path = log_path
        if os.path.exists(self.log_path):
            with open(log_path) as f:
                self.log = json.load(f)
        else:
            self.log = {}
            self.save()

    def save(self):
        with open(self.log_path, "w") as f:
            json.dump(self.log, f, indent=4)

    def create_session(self, module_name):
        self.log[module_name] = {}
        self.save()

    def update_info(self, module_name, key, value):
        if module_name not in self.log.keys():
            self.create_session(module_name)
        
        self.log[module_name][key] = value
        self.save()

    def get(self, module_name, key):
        if module_name not in self.log.keys():
            return None
        
        if key not in self.log[module_name].keys():
            return None
        
        return self.log[module_name][key]
    
    def get_session(self, module_name):
        if module_name not in self.log.keys():
            return None
        
        return self.log[module_name]
    