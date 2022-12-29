from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from view.widget_add_entry import AddEntryWidget
from view.widget_list_entry import ListEntryWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 150)
        self._setup_ui()

    def _setup_ui(self):
        self.stack = QStackedWidget()

        self.list_entry_widget = ListEntryWidget()
        self.list_entry_widget.btn_add_account.clicked.connect(
            self.on_clicked_add_account
        )
        self.add_account_widget = AddEntryWidget()
        self.add_account_widget.entry_added.connect(self.on_added_entry)
        self.add_account_widget.btn_cancel.clicked.connect(
            lambda: self.stack.setCurrentIndex(0)
        )
        self.stack.addWidget(self.list_entry_widget)
        self.stack.addWidget(self.add_account_widget)

        self.setCentralWidget(self.stack)
        self.setWindowTitle("TOTP Manager")

    def on_clicked_add_account(self):
        self.stack.setCurrentIndex(1)

    def on_added_entry(self):
        self.stack.setCurrentIndex(0)
