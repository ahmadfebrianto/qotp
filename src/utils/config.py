import json
import os
from configparser import ConfigParser

from utils.strings import String


class Config(ConfigParser):
    def __init__(self) -> None:
        super().__init__()

    @property
    def exists(self):
        return os.path.exists(String.APP_CONFIG_PATH)

    @property
    def is_db_path_valid(self):
        self.read()
        return os.path.exists(self.get("database", String.DB_PATH_KEY))

    def read(self):
        super().read(String.APP_CONFIG_PATH)

    def save(self):
        with open(String.APP_CONFIG_PATH, "w") as f:
            self.write(f)


config = Config()
