import json
import os
from configparser import ConfigParser

from utils.strings import String


class Config(ConfigParser):
    def __init__(self) -> None:
        super().__init__()

    @property
    def exists(self):
        return os.path.exists(String.CONFIG_PATH)

    @property
    def is_db_path_valid(self):
        self.read()
        return os.path.exists(
            self.get(String.CONFIG_SECTION_DB, String.CONFIG_KEY_DBPATH)
        )

    def read(self):
        super().read(String.CONFIG_PATH)

    def save(self):
        with open(String.CONFIG_PATH, "w") as f:
            self.write(f)


config = Config()
