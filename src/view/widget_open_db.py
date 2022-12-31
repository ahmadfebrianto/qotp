from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from model.db import db
from utils.config import config
from utils.constants import Constants
from utils.strings import String
from view.widget_file_dialog import FileDialogWidget


class OpenDBWidget(QWidget):

    db_opened = Signal()
    canceled = Signal()

    def __init__(self):
        super().__init__()
        config.read()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(String.TITLE_OPEN_DB)
        self.db_path = QLabel(String.LABEL_DB_PATH)
        self.db_path.setFixedWidth(Constants.LABEL_MAX_WIDTH)
        self.db_path_input = QLineEdit()
        self.db_path_input.setReadOnly(True)
        self.db_path_input.setPlaceholderText(String.PHOLDER_DB_LOCATION)
        self.db_path_input.setText(
            config[String.CONFIG_SECTION_DB][String.CONFIG_KEY_DBPATH]
        )
        self.db_path_dialog = QPushButton(String.BTN_DOTS)
        self.db_path_dialog.clicked.connect(self.open_db_location_dialog)

        self.hlayout_db_path = QHBoxLayout()
        self.hlayout_db_path.addWidget(self.db_path)
        self.hlayout_db_path.addWidget(self.db_path_input)
        self.hlayout_db_path.addWidget(self.db_path_dialog)

        self.db_password_label = QLabel(String.LABEL_DB_PASSWORD)
        self.db_password_label.setFixedWidth(Constants.LABEL_MAX_WIDTH)
        self.db_password_input = QLineEdit()
        self.db_password_input.setEchoMode(QLineEdit.Password)
        self.db_password_input.returnPressed.connect(self.open_db)

        self.hlayout_db_password = QHBoxLayout()
        self.hlayout_db_password.addWidget(self.db_password_label)
        self.hlayout_db_password.addWidget(self.db_password_input)

        # Cancel button
        self.cancel_btn = QPushButton(String.BTN_CANCEL)
        self.cancel_btn.setFixedWidth(Constants.LABEL_MAX_WIDTH)
        self.cancel_btn.clicked.connect(self.canceled.emit)

        # Create a button to create the database
        self.open_db_btn = QPushButton(String.BTN_OPEN_DB)
        self.open_db_btn.setFixedWidth(Constants.LABEL_MAX_WIDTH)
        self.open_db_btn.clicked.connect(self.open_db)

        # Create a horizontal layout and add the buttons
        self.hlayout_buttons = QHBoxLayout()
        self.hlayout_buttons.addWidget(self.cancel_btn)
        self.hlayout_buttons.addWidget(self.open_db_btn)

        # Create a vertical layout and add the horizontal layouts
        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout_db_path)
        self.vlayout.addLayout(self.hlayout_db_password)
        self.vlayout.addLayout(self.hlayout_buttons)

        self.setLayout(self.vlayout)

    def open_db_location_dialog(self):
        db = FileDialogWidget().load_db()
        if db:
            self.db_path_input.setText(db)

    def open_db(self):
        db_path = self.db_path_input.text()
        db_password = self.db_password_input.text()

        try:
            db.open(db_path, db_password)
        except Exception as e:
            self.db_password_input.setStyleSheet(
                "QLineEdit { border: 1px solid tomato; padding: 2px;}"
            )
            self.db_password_input.setToolTip(str(e))
            return
            
        config.set(String.CONFIG_SECTION_DB, String.CONFIG_KEY_DBPATH, db_path)
        config.save()
        self.db_opened.emit()
