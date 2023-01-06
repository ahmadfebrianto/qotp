from PySide6.QtCore import Qt, Signal
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
from utils.constants import Constants
from utils.strings import String
from view.widget_file_dialog import FileDialogWidget


class CreateDBWidget(QWidget):

    db_created = Signal()
    canceled = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(String.TITLE_CREATE_DB)
        self.setup_ui()

    def setup_ui(self):
        # Database name label and input
        self.label_db_name = QLabel(String.LABEL_DB_NAME)
        self.label_db_name.setFixedWidth(Constants.LABEL_MAX_WIDTH)
        self.input_db_name = QLineEdit()
        self.hlayout_db_name = QHBoxLayout()
        self.hlayout_db_name.addWidget(self.label_db_name)
        self.hlayout_db_name.addWidget(self.input_db_name)
        # Database location label and input
        self.label_db_location = QLabel(String.LABEL_DB_LOCATION)
        self.label_db_location.setFixedWidth(Constants.LABEL_MAX_WIDTH)
        self.input_db_location = QLineEdit()
        self.input_db_location.setReadOnly(True)
        self.input_db_location.setPlaceholderText(String.PHOLDER_DB_LOCATION)
        self.btn_open_file = QPushButton(String.BTN_DOTS)
        self.btn_open_file.setFixedWidth(Constants.BTN_WIDTH_DOTS)
        self.btn_open_file.clicked.connect(self.open_db_location_dialog)
        self.hlayout_db_location = QHBoxLayout()
        self.hlayout_db_location.addWidget(self.label_db_location)
        self.hlayout_db_location.addWidget(self.input_db_location)
        self.hlayout_db_location.addWidget(self.btn_open_file)
        # Database password label and input
        self.label_db_password = QLabel(String.LABEL_DB_PASSWORD)
        self.label_db_password.setFixedWidth(Constants.LABEL_MAX_WIDTH)
        self.input_db_password = QLineEdit()
        self.input_db_password.setEchoMode(QLineEdit.Password)
        self.hlayout_db_password = QHBoxLayout()
        self.hlayout_db_password.addWidget(self.label_db_password)
        self.hlayout_db_password.addWidget(self.input_db_password)
        # Database password confirm label and input
        self.label_db_password_confirm = QLabel(String.LABEL_DB_PASSWORD_CONFIRM)
        self.label_db_password_confirm.setFixedWidth(Constants.LABEL_MAX_WIDTH)
        self.input_db_password_confirm = QLineEdit()
        self.input_db_password_confirm.setEchoMode(QLineEdit.Password)
        self.input_db_password_confirm.returnPressed.connect(self.create_db)
        # Check if the passwords match
        self.input_db_password_confirm.textChanged.connect(self.check_passwords)
        self.hlayout_db_password_confirm = QHBoxLayout()
        self.hlayout_db_password_confirm.addWidget(self.label_db_password_confirm)
        self.hlayout_db_password_confirm.addWidget(self.input_db_password_confirm)
        # Cancel button
        self.btn_cancel = QPushButton(String.BTN_CANCEL)
        self.btn_cancel.setFixedWidth(Constants.BTN_WIDTH_NARROW)
        self.btn_cancel.clicked.connect(self.canceled.emit)
        # Database create button
        self.btn_create_db = QPushButton(String.BTN_CREATE_DB)
        self.btn_create_db.setFixedWidth(Constants.BTN_WIDTH_NARROW)
        self.btn_create_db.setEnabled(False)
        self.btn_create_db.clicked.connect(self.create_db)
        # Hlayout buttons setup
        self.hlayout_buttons = QHBoxLayout()
        self.hlayout_buttons.addWidget(self.btn_cancel)
        self.hlayout_buttons.addWidget(self.btn_create_db)
        self.hlayout_buttons.setSpacing(Constants.LAYOUT_SPACING)
        self.hlayout_buttons.setAlignment(Qt.AlignRight)
        # Layout setup
        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout_db_name)
        self.vlayout.addLayout(self.hlayout_db_location)
        self.vlayout.addLayout(self.hlayout_db_password)
        self.vlayout.addLayout(self.hlayout_db_password_confirm)
        self.vlayout.addStretch()
        self.vlayout.addLayout(self.hlayout_buttons)
        # Widget setup
        self.setLayout(self.vlayout)

    def open_db_location_dialog(self):
        label_db_location = FileDialogWidget().choose_db_location()
        self.input_db_location.setText(label_db_location)

    def create_db(self):
        if not self.btn_create_db.isEnabled():
            return
        # Get the database path
        db_path = get_db_path(
            self.input_db_location.text(), self.input_db_name.text(), String.APP_DB_EXT
        )
        db_password = self.input_db_password.text()
        # Create the database
        db.create(db_path, db_password)
        # Create config file after the database is created
        config.set(String.CONFIG_SECTION_DB, String.CONFIG_KEY_DBPATH, db_path)
        config.save()
        self.db_created.emit()

    def check_passwords(self):
        # If the passwords match, enable the create button. Otherwise, disable it.
        if self.input_db_password.text() == self.input_db_password_confirm.text():
            self.btn_create_db.setEnabled(True)
        else:
            self.btn_create_db.setEnabled(False)
