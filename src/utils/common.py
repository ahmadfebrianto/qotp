import os
import re

from .strings import String


def get_base_dir():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.normpath(base_dir)


def get_config_path():
    if os.name == String.WINDOWS:
        return os.path.join(
            os.environ[String.ENV_LOCALAPPDATA],
            String.APP_NAME_LOWER,
            String.CONFIG_FILENAME,
        )
    else:
        return os.path.join(
            os.environ[String.ENV_HOME],
            String.CONFIG_DIR_LINUX,
            String.APP_NAME_LOWER,
            String.CONFIG_FILENAME,
        )


def unpack_entry(entry):
    issuer, username = re.search(r"(.*) \((.*)\)", entry).groups()
    return issuer, username


def get_db_path(dir, name, ext):
    joined_path = os.path.join(dir, name + ext)
    return os.path.normpath(joined_path)


def load_stylesheet():
    style_file = os.path.join(get_base_dir(), String.APP_STYLESHEET)
    with open(style_file, "r") as f:
        return f.read()
