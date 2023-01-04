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
        parent = os.path.dirname(String.CONFIG_PATH)
        if not os.path.exists(parent):
            os.makedirs(parent)
        with open(String.CONFIG_PATH, "w") as f:
            self.write(f)

    def set(self, section, key, value):
        if not self.has_section(section):
            self.add_section(section)
        super().set(section, key, value)


config = Config()
