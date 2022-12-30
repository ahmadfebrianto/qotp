from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from model.db import db
from utils.common import get_db_path
from utils.config import config
from utils.strings import String
from view.widget_file_dialog import FileDialogWidget


class CreateDBWidget(QWidget):

    db_created = Signal()
    canceled = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(String.TITLE_CREATE_DB)
        self.setMinimumSize(600, 150)
        self.setup_ui()

    def setup_ui(self):
        label_max_width = 150
        # Database name label and input
        self.db_name = QLabel(String.LABEL_DB_NAME)
        self.db_name.setFixedWidth(label_max_width)
        self.db_name_input = QLineEdit()
        self.hlayout_db_name = QHBoxLayout()
        self.hlayout_db_name.addWidget(self.db_name)
        self.hlayout_db_name.addWidget(self.db_name_input)
        # Database location label and input
        self.db_location = QLabel(String.LABEL_DB_LOCATION)
        self.db_location.setFixedWidth(label_max_width)
        self.db_location_input = QLineEdit()
        self.db_location_input.setReadOnly(True)
        self.db_location_input.setPlaceholderText(String.PHOLDER_DB_LOCATION)
        self.db_location_dialog = QPushButton(String.BTN_DIALOG)
        self.db_location_dialog.clicked.connect(self._open_db_location_dialog)
        self.hlayout_db_location = QHBoxLayout()
        self.hlayout_db_location.addWidget(self.db_location)
        self.hlayout_db_location.addWidget(self.db_location_input)
        self.hlayout_db_location.addWidget(self.db_location_dialog)
        # Database password label and input
        self.db_password_label = QLabel(String.LABEL_DB_PASSWORD)
        self.db_password_label.setFixedWidth(label_max_width)
        self.db_password_input = QLineEdit()
        self.db_password_input.setEchoMode(QLineEdit.Password)
        self.hlayout_db_password = QHBoxLayout()
        self.hlayout_db_password.addWidget(self.db_password_label)
        self.hlayout_db_password.addWidget(self.db_password_input)
        # Database password confirm label and input
        self.db_password_confirm_label = QLabel(String.LABEL_DB_PASSWORD_CONFIRM)
        self.db_password_confirm_label.setFixedWidth(label_max_width)
        self.db_password_confirm_input = QLineEdit()
        self.db_password_confirm_input.setEchoMode(QLineEdit.Password)
        # Check if the passwords match
        self.db_password_confirm_input.textChanged.connect(self._check_passwords)
        self.hlayout_db_password_confirm = QHBoxLayout()
        self.hlayout_db_password_confirm.addWidget(self.db_password_confirm_label)
        self.hlayout_db_password_confirm.addWidget(self.db_password_confirm_input)
        # Cancel button
        self.cancel_btn = QPushButton(String.BTN_CANCEL)
        self.cancel_btn.clicked.connect(self.canceled.emit)
        # Database create button
        self.create_db_btn = QPushButton(String.BTN_CREATE_DB)
        self.create_db_btn.setEnabled(False)
        self.create_db_btn.clicked.connect(self._create_db)
        # Hlayout buttons setup
        self.hlayout_buttons = QHBoxLayout()
        self.hlayout_buttons.addWidget(self.cancel_btn)
        self.hlayout_buttons.addWidget(self.create_db_btn)
        # Layout setup
        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout_db_name)
        self.vlayout.addLayout(self.hlayout_db_location)
        self.vlayout.addLayout(self.hlayout_db_password)
        self.vlayout.addLayout(self.hlayout_db_password_confirm)
        self.vlayout.addLayout(self.hlayout_buttons)
        # Widget setup
        self.setLayout(self.vlayout)

    def _open_db_location_dialog(self):
        db_location = FileDialogWidget().choose_db_location()
        self.db_location_input.setText(db_location)

    def _create_db(self):
        # Get the database path
        db_path = get_db_path(
            self.db_location_input.text(), self.db_name_input.text(), String.APP_DB_EXT
        )
        db_password = self.db_password_input.text()

        # Create the database
        db.create(db_path, db_password)

        # Create config file after the database is created
        config["database"] = {}
        config["database"]["database_path"] = db_path
        config.save()

        self.db_created.emit(True)

    def _check_passwords(self):
        # If the passwords match, enable the create button. Otherwise, disable it.
        if self.db_password_input.text() == self.db_password_confirm_input.text():
            self.create_db_btn.setEnabled(True)
        else:
            self.create_db_btn.setEnabled(False)
