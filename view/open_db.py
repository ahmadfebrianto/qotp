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

from model import db
from utils import config


class OpenDBWindow(QMainWindow):

    data_ready = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Open an existing database")
        self.setMinimumSize(600, 150)
        self.setup_ui()
        self.__read_config()

    def setup_ui(self):
        label_max_width = 200
        widget = QWidget()
        self.setCentralWidget(widget)

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
        # Auto focus cursor on password input
        self.db_password_input.setFocus()

        hlayout_db_password = QHBoxLayout()
        hlayout_db_password.addWidget(self.db_password_label)
        hlayout_db_password.addWidget(self.db_password_input)

        # Create a button to create the database
        self.open_db_btn = QPushButton("Open database")
        self.open_db_btn.clicked.connect(self.__open_db)

        # Create a vertical layout and add the horizontal layouts
        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout_db_location)
        vlayout.addLayout(hlayout_db_password)
        vlayout.addWidget(self.open_db_btn)
        vlayout.setAlignment(self.open_db_btn, QtCore.Qt.AlignCenter)

        widget.setLayout(vlayout)

    def __open_db_location_dialog(self):
        db_location = QFileDialog.getExistingDirectory(
            self, "Select a location", self.config["db_path"] or "."
        )
        self.db_location_input.setText(db_location)

    def __open_db(self):
        db_path = self.db_location_input.text()
        db_password = self.db_password_input.text()
        db.open_db(db_path, db_password)
        self.data_ready.emit(db_path)
        self.close()

    def __read_config(self):
        self.config = config.read_config()
        self.db_location_input.setText(self.config["db_path"])

    def show(self) -> None:
        super().show()
        self.db_password_input.setFocus()
