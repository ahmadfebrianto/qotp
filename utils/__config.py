import json
from pathlib import Path


class Config:
    def __init__(self) -> None:
        self.path = Path.home() / ".config" / "otpy" / "otpy.conf"
        self.is_present = self.__check_config()

    def __check_config(self):
        if not self.path.exists():
            return False
        return True

    def create_config(self, db_path):
        config = {
            "db_path": db_path,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(config, f)

    def read_config(self):
        with open(self.path, "r") as f:
            config = json.load(f)
        return config
        
