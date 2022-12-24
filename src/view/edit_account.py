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
        # Set window frameless
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Username input
        self.username = QLineEdit()
        self.username.setPlaceholderText(String.PH_NEW_USERNAME)
        self.username.setText(self.old_username)
        # Save button
        btn_save = QPushButton(String.BTN_SAVE_USERNAME)
        btn_save.clicked.connect(self.save_changes)
        # Wrap widgets in layout
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.username)
        vlayout.addWidget(btn_save)
        # Set layout
        self.setLayout(vlayout)

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
