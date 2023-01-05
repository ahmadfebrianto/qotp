from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from utils.common import load_stylesheet
from utils.config import config
from utils.constants import Constants
from utils.strings import String
from view.widget_choose_action import ChooseActionWidget
from view.widget_create_db import CreateDBWidget
from view.widget_open_db import OpenDBWidget


class WelcomeWindow(QMainWindow):

    done = Signal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(*Constants.WINDOW_WELCOME_SIZE)
        self.setup_ui()
        self.setStyleSheet(load_stylesheet())
        self.show()
        self.setFixedSize(self.size())

    def setup_ui(self):
        # Choose action widget
        self.choose_action_widget = ChooseActionWidget()
        self.choose_action_widget.open_clicked.connect(self.show_open_db_widget)
        self.choose_action_widget.create_clicked.connect(self.show_create_db_widget)
        # Open db widget
        self.open_db_widget = OpenDBWidget()
        self.open_db_widget.db_opened.connect(self.on_done)
        self.open_db_widget.canceled.connect(self.on_cancel)
        # Create db widget
        self.create_db_widget = CreateDBWidget()
        self.create_db_widget.db_created.connect(self.on_done)
        self.create_db_widget.canceled.connect(self.on_cancel)
        # Stacked widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.choose_action_widget)
        self.stacked_widget.addWidget(self.open_db_widget)
        self.stacked_widget.addWidget(self.create_db_widget)
        self.stacked_widget.currentChanged.connect(self.on_current_changed)
        self.setCentralWidget(self.stacked_widget)

    def show(self):
        if not config.exists:
            self.show_choose_action_widget()
        elif config.exists and not config.is_db_path_valid:
            self.show_choose_action_widget()
        else:
            self.show_open_db_widget()

        screen = QApplication.primaryScreen().geometry()
        # Calculate the center point of the screen
        x = (screen.width() - self.width()) / 2
        y = (screen.height() - self.height()) / 2
        # Move the widget to the center of the screen
        self.move(x, y)
        super().show()

    def show_choose_action_widget(self):
        self.stacked_widget.setCurrentIndex(0)
        self.setWindowTitle(String.TITLE_CHOOSE_ACTION)

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

    def on_current_changed(self, w):
        widget = self.stacked_widget.widget(w)
        if widget == self.open_db_widget:
            widget.input_db_path.setText(
                config[String.CONFIG_SECTION_DB][String.CONFIG_KEY_DBPATH]
            )
            widget.input_db_password.setFocus()
