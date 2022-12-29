from PySide6 import QtCore
from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from utils.config import config
from view.create_db_widget import CreateDBWidget
from view.dialog import FileDialogWindow
from view.open_db_widget import OpenDBWidget


class CreateOrOpenDBWidget(QWidget):

    open_clicked = QtCore.Signal()
    create_clicked = QtCore.Signal()

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
        db_path = FileDialogWindow().load_db()
        if not db_path:
            return
        config["database"] = {}
        config["database"]["database_path"] = db_path
        self.open_clicked.emit()
        # self.close()

    def show_create_db_widget(self):
        self.create_clicked.emit()
        # self.close()


class WelcomeWindow(QMainWindow):

    done = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 150)
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setWindowTitle("Welcome")

        self.create_or_open_db_widget = CreateOrOpenDBWidget()
        self.create_or_open_db_widget.open_clicked.connect(self.show_open_db_widget)
        self.create_or_open_db_widget.create_clicked.connect(self.show_create_db_widget)

        self.open_db_widget = OpenDBWidget()
        self.open_db_widget.db_opened.connect(self.on_done)
        self.open_db_widget.canceled.connect(self.on_cancel)

        self.create_db_widget = CreateDBWidget()
        self.create_db_widget.db_created.connect(self.on_done)
        self.create_db_widget.canceled.connect(self.on_cancel)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.create_or_open_db_widget)
        self.stacked_widget.addWidget(self.open_db_widget)
        self.stacked_widget.addWidget(self.create_db_widget)

        self.setCentralWidget(self.stacked_widget)

    def show(self):
        super().show()
        if not config.exists:
            self.show_open_or_create_db_widget()
        elif config.exists and not config.is_db_path_valid:
            self.show_open_or_create_db_widget()
        else:
            self.show_open_db_widget()

    def show_open_or_create_db_widget(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_open_db_widget(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_create_db_widget(self):
        self.stacked_widget.setCurrentIndex(2)

    def on_cancel(self):
        self.show_open_or_create_db_widget()

    def on_done(self):
        self.done.emit()
        self.close()
