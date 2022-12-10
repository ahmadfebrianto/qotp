import json
import os
from pathlib import Path

from model.db import db
from utils.strings import String


class Config:
    def __init__(self) -> None:
        self.path = Path(String.APP_CONFIG_PATH)

    @property
    def exists(self):
        if not self.path.exists():
            return False
        return True

    def create(self):
        config = {
            String.DB_PATH_KEY: db.db_path,
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
