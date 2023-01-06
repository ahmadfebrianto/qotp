import os
from configparser import ConfigParser

from utils.common import get_config_path
from utils.strings import String


class Config(ConfigParser):
    def __init__(self) -> None:
        self.config_path = get_config_path()
        super().__init__()

    @property
    def exists(self):
        return os.path.exists(self.config_path)

    @property
    def is_db_path_valid(self):
        self.read()
        return os.path.exists(
            self.get(String.CONFIG_SECTION_DB, String.CONFIG_KEY_DBPATH)
        )

    def read(self):
        super().read(self.config_path)

    def save(self):
        parent = os.path.dirname(self.config_path)
        if not os.path.exists(parent):
            os.makedirs(parent)
        with open(self.config_path, "w") as f:
            self.write(f)

    def set(self, section, key, value):
        if not self.has_section(section):
            self.add_section(section)
        super().set(section, key, value)


config = Config()
