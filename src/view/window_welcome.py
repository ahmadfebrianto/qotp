from PySide6 import QtCore
from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from utils.config import config
from view.widget_choose_action import ChooseActionWidget
from view.widget_create_db import CreateDBWidget
from view.widget_file_dialog import FileDialogWidget
from view.widget_open_db import OpenDBWidget


class WelcomeWindow(QMainWindow):

    done = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 150)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setWindowTitle("Welcome")

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
            self.show_open_or_create_db_widget()
        elif config.exists and not config.is_db_path_valid:
            self.show_open_or_create_db_widget()
        else:
            self.show_open_db_widget()

    def show_open_or_create_db_widget(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_open_db_widget(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_create_db_widget(self):
        self.stacked_widget.setCurrentIndex(2)

    def on_cancel(self):
        self.show_open_or_create_db_widget()

    def on_done(self):
        self.done.emit()
        self.close()
