import sys

from PySide6.QtWidgets import QApplication

from utils.config import config
from utils.strings import String
from view.create_db import CreateDBWindow
from view.dialog import FileDialogWindow
from view.main_window import MainWindow
from view.open_db import OpenDBWindow
from view.welcome import Welcome


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.start()

    def start(self):
        if not config.exists:
            self.welcome()
        elif config.exists and not config.is_db_path_valid:
            self.welcome()
        else:
            self.open_open_db_window()

    def welcome(self):
        self.welcome_window = Welcome()
        self.welcome_window.show()
        self.welcome_window.signal_create.connect(self.open_create_db_window)
        self.welcome_window.signal_open.connect(self.open_open_db_window)

    def open_open_db_window(self):
        self.open_db_window = OpenDBWindow()
        self.open_db_window.show()
        self.open_db_window.closeEvent = self.open_main_window

    def open_create_db_window(self):
        self.create_db_window = CreateDBWindow()
        self.create_db_window.show()
        self.create_db_window.closeEvent = self.open_main_window

    def open_main_window(self, event=None):
        self.main_window = MainWindow()
        self.main_window.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
