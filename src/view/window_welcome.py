from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from utils.config import config
from utils.strings import String
from view.widget_choose_action import ChooseActionWidget
from view.widget_create_db import CreateDBWidget
from view.widget_open_db import OpenDBWidget


class WelcomeWindow(QMainWindow):

    done = Signal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 150)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.choose_action_widget = ChooseActionWidget()
        self.choose_action_widget.open_clicked.connect(self.show_open_db_widget)
        self.choose_action_widget.create_clicked.connect(self.show_create_db_widget)

        self.open_db_widget = OpenDBWidget()
        self.open_db_widget.db_opened.connect(self.on_done)
        self.open_db_widget.canceled.connect(self.on_cancel)

        self.create_db_widget = CreateDBWidget()
        self.create_db_widget.db_created.connect(self.on_done)
        self.create_db_widget.canceled.connect(self.on_cancel)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.choose_action_widget)
        self.stacked_widget.addWidget(self.open_db_widget)
        self.stacked_widget.addWidget(self.create_db_widget)

        self.setCentralWidget(self.stacked_widget)

    def show(self):
        super().show()
        if not config.exists:
            self.show_choose_action_widget()
        elif config.exists and not config.is_db_path_valid:
            self.show_choose_action_widget()
        else:
            self.show_open_db_widget()

    def show_choose_action_widget(self):
        self.stacked_widget.setCurrentIndex(0)
        self.setWindowTitle(String.TITLE_WELCOME)

    def show_open_db_widget(self):
        self.stacked_widget.setCurrentIndex(1)
        self.setWindowTitle(String.TITLE_OPEN_DB)

    def show_create_db_widget(self):
        self.stacked_widget.setCurrentIndex(2)
        self.setWindowTitle(String.TITLE_CREATE_DB)

    def on_cancel(self):
        self.show_choose_action_widget()

    def on_done(self):
        self.done.emit()
        self.close()
