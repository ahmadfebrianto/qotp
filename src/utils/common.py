import os

import plyer
import pyotp
from PySide6.QtWidgets import QApplication


def show_notification(app_name, message):
    plyer.notification.notify(
        title=app_name,
        message=message,
        app_name=app_name,
        timeout=1,
    )


def get_config_path(app_name, app_config_name):
    if os.name == "nt":
        return os.path.join(os.environ["LOCALAPPDATA"], app_name, app_config_name)
    else:
        return os.path.join(os.environ["HOME"], ".config", app_name, app_config_name)


def copy_to_clipboard(text):
    clipboard = QApplication.clipboard()
    clipboard.setText(text)
