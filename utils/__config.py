import json
import os
from pathlib import Path

from model import db


class Config:
    def __init__(self) -> None:
        if os.name == "nt":
            self.path = Path(os.environ["LOCALAPPDATA"], "otpy", "config.json")
        else:
            self.path = Path.home() / ".config" / "otpy" / "otpy.conf"
        self.is_present = self.__check_config()

    def __check_config(self):
        if not self.path.exists():
            return False
        return True

    def create_config(self):
        config = {
            "db_path": db.db_path,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(config, f)

    def read_config(self):
        with open(self.path, "r") as f:
            config = json.load(f)
        return config

    def update_config(self, config):
        with open(self.path, "w") as f:
            json.dump(config, f)
