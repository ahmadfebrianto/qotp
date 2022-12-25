from PySide6 import QtCore
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from model.db import db
from utils.config import config
from utils.strings import String


class CreateDBWindow(QMainWindow):
    data_ready = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(String.CREATE_DB_TITLE)
        self.setMinimumSize(600, 150)
        self.setup_ui()

    def setup_ui(self):
        label_max_width = 150
        # Database name label and input
        self.db_name = QLabel(String.LABEL_DB_NAME)
        self.db_name.setFixedWidth(label_max_width)
        self.db_name_input = QLineEdit()
        hlayout_db_name = QHBoxLayout()
        hlayout_db_name.addWidget(self.db_name)
        hlayout_db_name.addWidget(self.db_name_input)

        # Database location label and input
        self.db_location = QLabel(String.LABEL_DB_LOCATION)
        self.db_location.setFixedWidth(label_max_width)
        self.db_location_input = QLineEdit()
        self.db_location_input.setReadOnly(True)
        self.db_location_input.setPlaceholderText(String.PH_DB_LOCATION)
        self.db_location_dialog = QPushButton(String.BTN_DIALOG)
        self.db_location_dialog.clicked.connect(self._open_db_location_dialog)
        hlayout_db_location = QHBoxLayout()
        hlayout_db_location.addWidget(self.db_location)
        hlayout_db_location.addWidget(self.db_location_input)
        hlayout_db_location.addWidget(self.db_location_dialog)

        # Database password label and input
        self.db_password_label = QLabel(String.LABEL_DB_PASSWORD)
        self.db_password_label.setFixedWidth(label_max_width)
        self.db_password_input = QLineEdit()
        self.db_password_input.setEchoMode(QLineEdit.Password)
        hlayout_db_password = QHBoxLayout()
        hlayout_db_password.addWidget(self.db_password_label)
        hlayout_db_password.addWidget(self.db_password_input)

        # Database password confirm label and input
        self.db_password_confirm_label = QLabel(String.LABEL_DB_PASSWORD_CONFIRM)
        self.db_password_confirm_label.setFixedWidth(label_max_width)
        self.db_password_confirm_input = QLineEdit()
        self.db_password_confirm_input.setEchoMode(QLineEdit.Password)
        # Check if the passwords match
        self.db_password_confirm_input.textChanged.connect(self._check_passwords)
        hlayout_db_password_confirm = QHBoxLayout()
        hlayout_db_password_confirm.addWidget(self.db_password_confirm_label)
        hlayout_db_password_confirm.addWidget(self.db_password_confirm_input)

        # Database create button
        self.create_db_btn = QPushButton(String.BTN_CREATE_DB)
        self.create_db_btn.setEnabled(False)
        self.create_db_btn.clicked.connect(self._create_db)

        # Layout setup
        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout_db_name)
        vlayout.addLayout(hlayout_db_location)
        vlayout.addLayout(hlayout_db_password)
        vlayout.addLayout(hlayout_db_password_confirm)
        vlayout.addWidget(self.create_db_btn)

        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)

    def _open_db_location_dialog(self):
        db_location = QFileDialog.getExistingDirectory(self, String.DB_DIALOG_TITLE)
        self.db_location_input.setText(db_location)

    def _create_db(self):
        # Get the database path
        self.db_path = String.get_db_path(
            self.db_location_input.text(), self.db_name_input.text()
        )

        # Create the database
        db.create(self.db_path, self.db_password_input.text())

        # Create config file after the database is created
        config.create()

        # self.data_ready.emit(db)
        self.close()

    def _check_passwords(self):
        # If the passwords match, enable the create button. Otherwise, disable it.
        if self.db_password_input.text() == self.db_password_confirm_input.text():
            self.create_db_btn.setEnabled(True)
        else:
            self.create_db_btn.setEnabled(False)
