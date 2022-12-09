import sys

from PySide6.QtWidgets import (
    QApplication,
)

from utils.config import config
from view.create_db import CreateDBWindow
from view.main_window import MainWindow
from view.open_db import OpenDBWindow


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.main_window = None

        if not config.exists:
            self.create_db_window = CreateDBWindow()
            self.create_db_window.data_ready.connect(self.open_main_window)
            self.create_db_window.show()

        else:
            self.open_db_window = OpenDBWindow()
            self.open_db_window.data_ready.connect(self.open_main_window)
            self.open_db_window.show()

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
