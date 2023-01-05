import re

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QWidget

from model.db import db
from utils.common import load_stylesheet
from utils.constants import Constants
from utils.strings import String


class EditEntryWidget(QWidget):

    edit_done = Signal()

    def __init__(self, entry):
        super().__init__()
        self.selected_entry = entry
        issuer, username = re.search(r"(.*) \((.*)\)", self.selected_entry).groups()
        self.old_issuer = issuer
        self.old_username = username
        self.setWindowTitle(String.TITLE_EDIT_ENTRY)
        self.setMinimumSize(*Constants.WINDOW_EDIT_ENTRY_SIZE)
        self.setup_ui()
        self.setStyleSheet(load_stylesheet())

    def setup_ui(self):
        # Set window frameless
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Issuer input
        self.input_issuer = QLineEdit()
        self.input_issuer.setPlaceholderText(String.PHOLDER_NEW_ISSUER)
        self.input_issuer.setText(self.old_issuer)
        # Username input
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText(String.PHOLDER_NEW_USERNAME)
        self.input_username.setText(self.old_username)
        # Save button
        self.btn_save = QPushButton(String.BTN_SAVE_USERNAME)
        self.btn_save.clicked.connect(self.save_changes)
        # Wrap widgets in layout
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.input_issuer)
        self.vlayout.addWidget(self.input_username)
        self.vlayout.addWidget(self.btn_save)
        # Set layout
        self.setLayout(self.vlayout)

    def save_changes(self):
        new_issuer = self.input_issuer.text()
        new_username = self.input_username.text()
        if self.old_issuer == new_issuer and self.old_username == new_username:
            self.close()
            return
        elif new_issuer == "" or new_username == "":
            return
        db.update_entry(self.selected_entry, new_issuer, new_username)
        self.edit_done.emit()
        self.close()

    # Define key events
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

        if event.key() == Qt.Key_Return:
            self.save_changes()
