from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget


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

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.btn_open_db)
        vlayout.addWidget(self.btn_create_db)

        widget = QWidget()
        widget.setLayout(vlayout)

        self.setCentralWidget(widget)

    def on_clicked_open(self):
        self.signal_open.emit()
        self.close()

    def on_clicked_create(self):
        self.signal_create.emit()
        self.close()
