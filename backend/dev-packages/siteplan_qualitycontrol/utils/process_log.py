"""
Class LogJson for the siteplan quality control log control.

"""

import os
import json
from pathlib import Path


class LogJson():
    """
    Class for the task log.
    """
    def __init__(self, log_path=None):
        self.log_path = log_path
        if os.path.exists(self.log_path):
            with open(log_path) as f:
                self.log_json = json.load(f)
        else:
            self.log_json = {}
            self.save()
        
    def save(self):
        with open(self.log_path, "w") as f:
            json.dump(self.log_json, f, indent=4)

    def update(self, key, value):
        self.log_json[key] = value
        self.save()

    def check(self, key):
        if key in self.log_json:
            return self.log_json[key]
        
        return False


