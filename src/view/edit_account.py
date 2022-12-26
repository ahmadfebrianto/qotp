from PySide6.QtCore import Qt
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
        # Set window frameless
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Username input
        self.username = QLineEdit()
        self.username.setPlaceholderText(String.PH_NEW_USERNAME)
        self.username.setText(self.old_username)
        # Save button
        self.btn_save = QPushButton(String.BTN_SAVE_USERNAME)
        self.btn_save.clicked.connect(self.save_changes)
        # Wrap widgets in layout
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.username)
        self.vlayout.addWidget(self.btn_save)
        # Set layout
        self.setLayout(self.vlayout)

    def save_changes(self):
        new_username = self.username.text()
        if new_username:
            db.update_entry(self.old_username, new_username)
            self.close()

    # Define key events
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

        if event.key() == Qt.Key_Return:
            self.save_changes()
