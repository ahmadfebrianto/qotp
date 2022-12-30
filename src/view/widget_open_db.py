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
from view.widget_file_dialog import FileDialogWidget


class OpenDBWidget(QWidget):

    db_opened = Signal()
    canceled = Signal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 150)
        config.read()
        self._setup_ui()

    def _setup_ui(self):
        label_max_width = 150

        self.setWindowTitle("Open an existing database")
        self.db_path = QLabel("Database path")
        self.db_path.setFixedWidth(label_max_width)
        self.db_path_input = QLineEdit()
        self.db_path_input.setReadOnly(True)
        self.db_path_input.setPlaceholderText("Select a location")
        self.db_path_input.setText(config["database"]["database_path"])
        self.db_path_dialog = QPushButton("...")
        self.db_path_dialog.clicked.connect(self._open_db_location_dialog)

        self.hlayout_db_path = QHBoxLayout()
        self.hlayout_db_path.addWidget(self.db_path)
        self.hlayout_db_path.addWidget(self.db_path_input)
        self.hlayout_db_path.addWidget(self.db_path_dialog)

        self.db_password_label = QLabel("Database password")
        self.db_password_label.setFixedWidth(label_max_width)
        self.db_password_input = QLineEdit()
        self.db_password_input.setEchoMode(QLineEdit.Password)
        self.db_password_input.returnPressed.connect(self._open_db)

        # Auto focus cursor on password input
        self.db_password_input.setFocus()

        self.hlayout_db_password = QHBoxLayout()
        self.hlayout_db_password.addWidget(self.db_password_label)
        self.hlayout_db_password.addWidget(self.db_password_input)

        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedWidth(label_max_width)
        self.cancel_btn.clicked.connect(self.canceled.emit)

        # Create a button to create the database
        self.open_db_btn = QPushButton("Open database")
        self.open_db_btn.setFixedWidth(label_max_width)
        self.open_db_btn.clicked.connect(self._open_db)

        # Create a horizontal layout and add the buttons
        self.hlayout_buttons = QHBoxLayout()
        self.hlayout_buttons.addWidget(self.cancel_btn)
        self.hlayout_buttons.addWidget(self.open_db_btn)

        # Create a vertical layout and add the horizontal layouts
        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout_db_path)
        self.vlayout.addLayout(self.hlayout_db_password)
        self.vlayout.addLayout(self.hlayout_buttons)
        # self.vlayout.setAlignment(self.open_db_btn, QtCore.Qt.AlignCenter)

        self.setLayout(self.vlayout)

    def _open_db_location_dialog(self):
        db = FileDialogWidget().load_db()
        if db:
            self.db_path_input.setText(db)

    def _open_db(self):
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
        config["database"]["database_path"] = db_path
        config.save()
        self.db_opened.emit(True)
        self.close()

    def show(self) -> None:
        super().show()
        # Get the screen geometry
        screen = QApplication.primaryScreen().geometry()
        # Calculate the center point of the screen
        x = (screen.width() - self.width()) / 2
        y = (screen.height() - self.height()) / 2
        # Move the self.widget to the center of the screen
        self.move(x, y)
        if config.is_db_path_valid:
            self.db_password_input.setFocus()
