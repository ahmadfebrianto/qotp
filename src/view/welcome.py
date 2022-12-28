from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

from utils.config import config
from view.dialog import FileDialogWindow


class Welcome(QMainWindow):

    signal_open = QtCore.Signal()
    signal_create = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 150)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Welcome")

        self.btn_open_db = QPushButton("Open an existing database")
        self.btn_open_db.clicked.connect(self.on_clicked_open)

        self.btn_create_db = QPushButton("Create a new database")
        self.btn_create_db.clicked.connect(self.on_clicked_create)

        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.btn_open_db)
        self.vlayout.addWidget(self.btn_create_db)

        self.widget = QWidget()
        self.widget.setLayout(self.vlayout)

        self.setCentralWidget(self.widget)

    def on_clicked_open(self):
        db_path = FileDialogWindow().load_db()
        if not db_path:
            return
        config["database"] = {}
        config["database"]["database_path"] = db_path
        self.signal_open.emit()
        self.close()

    def on_clicked_create(self):
        self.signal_create.emit()
        self.close()
