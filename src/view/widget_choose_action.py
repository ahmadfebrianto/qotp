from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from utils.config import config
from view.widget_file_dialog import FileDialogWidget


class ChooseActionWidget(QWidget):

    open_clicked = Signal()
    create_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 150)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Welcome")

        self.btn_open_db = QPushButton("Open an existing database")
        self.btn_open_db.clicked.connect(self.show_open_db_widget)

        self.btn_create_db = QPushButton("Create a new database")
        self.btn_create_db.clicked.connect(self.show_create_db_widget)

        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.btn_open_db)
        self.vlayout.addWidget(self.btn_create_db)

        self.setLayout(self.vlayout)

    def show_open_db_widget(self):
        db_path = FileDialogWidget().load_db()
        if not db_path:
            return
        config["database"] = {}
        config["database"]["database_path"] = db_path
        self.open_clicked.emit()

    def show_create_db_widget(self):
        self.create_clicked.emit()
