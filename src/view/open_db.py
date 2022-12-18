from pathlib import Path

from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
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


class OpenDBWindow(QMainWindow):

    data_ready = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 150)
        self.config = config.read()
        self.__setup_ui()

    def __setup_ui(self):
        label_max_width = 150
        widget = QWidget()
        self.setCentralWidget(widget)

        if not self.__is_db_path_valid(self.config["db_path"]):
            self.setWindowTitle("Create or Open an existing database")
            db_path = self.config["db_path"]
            self.db_not_found_label = QLabel(f"Database '{db_path}' not found!")
            self.db_not_found_label.setStyleSheet(
                "QLabel { border: 1px solid tomato; color: tomato; font-weight: bold;}"
            )
            self.db_not_found_label.setFixedHeight(50)
            self.db_not_found_label.setAlignment(
                QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
            )

            btn_create_db = QPushButton("Create a new database")
            btn_create_db.clicked.connect(self.__create_db)

            btn_open_db = QPushButton("Open another existing database")
            btn_open_db.clicked.connect(self.__open_db_location_dialog)

            hlayout = QHBoxLayout()
            hlayout.addWidget(btn_create_db)
            hlayout.addWidget(btn_open_db)

            layout = QVBoxLayout()
            layout.addWidget(self.db_not_found_label)
            layout.addLayout(hlayout)

            widget.setLayout(layout)

        else:
            self.setWindowTitle("Open an existing database")
            self.db_path = QLabel("Database path")
            self.db_path.setFixedWidth(label_max_width)
            self.db_path_input = QLineEdit()
            self.db_path_input.setReadOnly(True)
            self.db_path_input.setPlaceholderText("Select a location")
            self.db_path_input.setText(self.config["db_path"])
            self.db_path_dialog = QPushButton("...")
            self.db_path_dialog.clicked.connect(self.__open_db_location_dialog)

            hlayout_db_path = QHBoxLayout()
            hlayout_db_path.addWidget(self.db_path)
            hlayout_db_path.addWidget(self.db_path_input)
            hlayout_db_path.addWidget(self.db_path_dialog)

            self.db_password_label = QLabel("Database password")
            self.db_password_label.setFixedWidth(label_max_width)
            self.db_password_input = QLineEdit()
            self.db_password_input.setEchoMode(QLineEdit.Password)
            self.db_password_input.returnPressed.connect(self.__open_db)

            # Auto focus cursor on password input
            self.db_password_input.setFocus()

            hlayout_db_password = QHBoxLayout()
            hlayout_db_password.addWidget(self.db_password_label)
            hlayout_db_password.addWidget(self.db_password_input)

            # Create a button to create the database
            self.open_db_btn = QPushButton("Open database")
            self.open_db_btn.setFixedWidth(label_max_width)
            self.open_db_btn.clicked.connect(self.__open_db)

            # Create a vertical layout and add the horizontal layouts
            vlayout = QVBoxLayout()
            vlayout.addLayout(hlayout_db_path)
            vlayout.addLayout(hlayout_db_password)
            vlayout.addWidget(self.open_db_btn)
            vlayout.setAlignment(self.open_db_btn, QtCore.Qt.AlignCenter)

            widget.setLayout(vlayout)

    def __open_db_location_dialog(self):
        db = QFileDialog.getOpenFileName(
            self, "Open database", "", "KeePass database (*.kdbx)"
        )

        if not self.__is_db_path_valid(self.config["db_path"]):
            self.config["db_path"] = db[0]
            self.__setup_ui()
            self.show()

    def __open_db(self):
        db_path = self.db_path_input.text()
        self.config["db_path"] = db_path
        config.update(self.config)
        db_password = self.db_password_input.text()

        try:
            db.open(db_path, db_password)

        except Exception as e:
            self.db_password_input.setStyleSheet(
                "QLineEdit { border: 1px solid tomato; padding: 2px;}"
            )
            self.db_password_input.setToolTip(str(e))
            return

        self.data_ready.emit(db_path)
        self.close()

    def __is_db_path_valid(self, path):
        db_path = Path(path)
        if not db_path.exists():
            return False
        return True

    def __create_db(self):
        from view.create_db import CreateDBWindow

        self.create_db_window = CreateDBWindow()
        self.create_db_window.data_ready.connect(self.close)
        self.create_db_window.show()

    def show(self) -> None:
        super().show()
        # Get the screen geometry
        screen = QApplication.primaryScreen().geometry()

        # Calculate the center point of the screen
        x = (screen.width() - self.width()) / 2
        y = (screen.height() - self.height()) / 2

        # Move the widget to the center of the screen
        self.move(x, y)

        if self.__is_db_path_valid(self.config["db_path"]):
            self.db_password_input.setFocus()

    def close(self):
        self.data_ready.emit("")
        super().close()
