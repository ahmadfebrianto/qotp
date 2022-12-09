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

from utils.config import config


class CreateDBWindow(QMainWindow):

    data_ready = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create a new database")
        self.setMinimumSize(600, 150)
        self.setup_ui()

    def setup_ui(self):
        label_max_width = 200
        widget = QWidget()
        self.setCentralWidget(widget)

        # Create input for db name and db dialog location
        self.db_name = QLabel("Database name")
        # Make this label width the same as the other labels
        self.db_name.setFixedWidth(label_max_width)
        self.db_name_input = QLineEdit()

        hlayout_db_name = QHBoxLayout()
        hlayout_db_name.addWidget(self.db_name)
        hlayout_db_name.addWidget(self.db_name_input)

        self.db_location = QLabel("Database location")
        self.db_location.setFixedWidth(label_max_width)
        self.db_location_input = QLineEdit()
        self.db_location_input.setReadOnly(True)
        self.db_location_input.setPlaceholderText("Select a location")
        self.db_location_dialog = QPushButton("...")
        self.db_location_dialog.clicked.connect(self.__open_db_location_dialog)

        hlayout_db_location = QHBoxLayout()
        hlayout_db_location.addWidget(self.db_location)
        hlayout_db_location.addWidget(self.db_location_input)
        hlayout_db_location.addWidget(self.db_location_dialog)

        self.db_password_label = QLabel("Database password")
        self.db_password_label.setFixedWidth(label_max_width)
        self.db_password_input = QLineEdit()
        self.db_password_input.setEchoMode(QLineEdit.Password)

        hlayout_db_password = QHBoxLayout()
        hlayout_db_password.addWidget(self.db_password_label)
        hlayout_db_password.addWidget(self.db_password_input)

        self.db_password_confirm_label = QLabel("Confirm password")
        self.db_password_confirm_label.setFixedWidth(label_max_width)
        self.db_password_confirm_input = QLineEdit()
        self.db_password_confirm_input.setEchoMode(QLineEdit.Password)

        # Check if the passwords match
        self.db_password_confirm_input.textChanged.connect(self.__check_passwords)

        hlayout_db_password_confirm = QHBoxLayout()
        hlayout_db_password_confirm.addWidget(self.db_password_confirm_label)
        hlayout_db_password_confirm.addWidget(self.db_password_confirm_input)

        # Create database button
        self.create_db_btn = QPushButton("Create database")
        self.create_db_btn.setEnabled(False)
        self.create_db_btn.clicked.connect(self.__create_db)

        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout_db_name)
        vlayout.addLayout(hlayout_db_location)
        vlayout.addLayout(hlayout_db_password)
        vlayout.addLayout(hlayout_db_password_confirm)
        vlayout.addWidget(self.create_db_btn)

        widget.setLayout(vlayout)

    def __open_db_location_dialog(self):
        # Get the location of the database
        db_location = QFileDialog.getExistingDirectory(
            self, "Select a location for the database"
        )
        self.db_location_input.setText(db_location)

    def __create_db(self):
        # Create the database
        from model import db

        self.db_path = (
            f"{self.db_location_input.text()}/{self.db_name_input.text()}.kdbx"
        )

        db.create_db(
            self.db_path,
            self.db_password_input.text(),
        )

        # Create config file
        config.create()

        self.data_ready.emit(db)
        self.close()

    def __check_passwords(self):
        # Check if the passwords match
        if self.db_password_input.text() == self.db_password_confirm_input.text():
            self.create_db_btn.setEnabled(True)
        else:
            self.create_db_btn.setEnabled(False)
