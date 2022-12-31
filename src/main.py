import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from utils.strings import String
from view.window_main import MainWindow
from view.window_welcome import WelcomeWindow


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
    app.setWindowIcon(QIcon(String.APP_ICON))
    sys.exit(app.exec())
