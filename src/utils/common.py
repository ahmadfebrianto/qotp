import os
import re


def get_config_path(app_name, app_config_name):
    WIN = "nt"
    WIN_DIR = "LOCALAPPDATA"
    LINUX_HOME = "HOME"
    LINUX_DIR = ".config"
    if os.name == WIN:
        return os.path.join(os.environ[WIN_DIR], app_name, app_config_name)
    else:
        return os.path.join(
            os.environ[LINUX_HOME], LINUX_DIR, app_name, app_config_name
        )


def unpack_entry(entry):
    issuer, username = re.search(r"(.*) \((.*)\)", entry).groups()
    return issuer, username


def get_db_path(dir, name, ext):
    joined_path = os.path.join(dir, name + ext)
    return os.path.normpath(joined_path)


def load_stylesheet():
    style_file = "assets/css/styles.css"
    with open(style_file, "r") as f:
        return f.read()
