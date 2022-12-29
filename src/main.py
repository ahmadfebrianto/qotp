import sys

from PySide6.QtWidgets import QApplication

from utils.config import config
from view.main_window import MainWindow
from view.welcome_window import WelcomeWindow


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.welcome_window = None
        self.main_window = None
        self.open_welcome_window()

    def open_welcome_window(self, event=None):
        self.welcome_window = WelcomeWindow()
        self.welcome_window.show()
        self.welcome_window.done.connect(self.open_main_window)

    def open_main_window(self, event=None):
        self.main_window = MainWindow()
        self.main_window.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
