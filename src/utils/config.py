import json
import os
from pathlib import Path

from model.db import db


class Config:
    def __init__(self) -> None:
        if os.name == "nt":
            self.path = Path(os.environ["LOCALAPPDATA"], "otpy", "config.json")
        else:
            self.path = Path.home() / ".config" / "otpy" / "otpy.conf"

    @property
    def exists(self):
        if not self.path.exists():
            return False
        return True

    def create(self):
        config = {
            "db_path": db.db_path,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(config, f)

    def read(self):
        with open(self.path, "r") as f:
            config = json.load(f)
        return config

    def update(self, config):
        with open(self.path, "w") as f:
            json.dump(config, f)


config = Config()
