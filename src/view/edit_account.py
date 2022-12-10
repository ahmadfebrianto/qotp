from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QWidget

from model.db import db
from utils.strings import String


class EditAccountWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.old_username = username
        self.setWindowTitle(String.EDIT_ACCOUNT_TITLE)
        self.setMinimumSize(300, 100)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.esc = QShortcut(QKeySequence("Esc"), self)
        self.esc.activated.connect(self.close)

        self.username = QLineEdit()
        self.username.setPlaceholderText(String.PH_NEW_USERNAME)
        self.username.setText(self.old_username)
        self.username.returnPressed.connect(self.save_changes)

        btn_save = QPushButton(String.BTN_SAVE_USERNAME)
        btn_save.clicked.connect(self.save_changes)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.username)
        vlayout.addWidget(btn_save)

        self.setLayout(vlayout)

    def save_changes(self):
        new_username = self.username.text()
        if new_username:
            account = db.instance.find_entries_by_username(self.old_username)[0]
            account.username = new_username
            db.instance.save()
            self.close()
