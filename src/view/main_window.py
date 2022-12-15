from time import sleep
from urllib.parse import unquote

import pyotp
from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from model.db import db
from utils.common import parse_uri, show_notification
from utils.strings import String


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.edit_username_window = None
        self.add_account_window = None
        self.list_widget = None
        self.setWindowTitle(String.APP_NAME)
        self.setMinimumSize(600, 400)
        self.setup_ui()
        self.accounts = {}
        self.hashes = []
        self.load_accounts()
        self.key_pressed = False
        self.timer = QtCore.QElapsedTimer()

    def setup_ui(self):
        widget = QWidget()
        self.setCentralWidget(widget)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.copy_otp_code)
        self.list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_menu)
        self.list_widget.setStyleSheet("QListWidget::item { padding: 10px; }")

        btn_add_account = QPushButton(String.BUTTON_ADD_ACCOUNT)
        btn_add_account.clicked.connect(self.open_add_account_window)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.list_widget)
        vlayout.addWidget(btn_add_account)

        widget.setLayout(vlayout)

    def show_menu(self, position):
        from PySide6.QtWidgets import QMenu

        menu = QMenu()
        menu.addAction(String.CTX_MENU_COPY, self.copy_otp_code)
        menu.addAction(String.CTX_MENU_EXPORT, self.open_export_account_window)
        menu.addAction(String.CTX_MENU_EDIT, self.open_edit_account_window)
        menu.addAction(String.CTX_MENU_DELETE, self.delete_account)
        menu.exec(self.list_widget.mapToGlobal(position))

    def open_add_account_window(self):
        from view.add_account import AddAccountWindow

        self.add_account_window = AddAccountWindow()
        self.add_account_window.data_ready.connect(self.add_account)
        self.add_account_window.show()

    def open_export_account_window(self):
        from view.export_account import ExportAccountWindow
        
        current_item = self.list_widget.currentItem()
        chosen_account = self.accounts[current_item.text()]
        self.export_account_window = ExportAccountWindow(self, chosen_account)
        self.export_account_window.show()

    def add_account(self, uri):
        uri = unquote(uri)
        uri_hash = self.get_digest(uri)
        if uri_hash in self.hashes:
            QMessageBox.warning(
                self,
                String.WARNING_DUPLICATE_ENTRY,
                String.WARNING_DUPLICATE_ENTRY_BODY,
            )
            return

        parsed_uri = parse_uri(uri)
        title = parsed_uri.issuer
        username = parsed_uri.name
        password = parsed_uri.secret
        url = uri

        db.instance.add_entry(
            db.instance.root_group, title, username, password, url=url
        )
        db.instance.save()

        self.update_accounts()

    def copy_otp_code(self, item=None):
        if not item:
            item = self.list_widget.currentItem()
        clicked_account = self.accounts[item.text()]
        parsed_uri = pyotp.parse_uri(clicked_account.url)
        otp_code = parsed_uri.now()
        QApplication.clipboard().setText(otp_code)

        show_notification(String.APP_NAME, String.NOTIF_COPY_SUCCESS)

        sleep(1)
        self.close()

    def get_digest(self, uri):
        from hashlib import sha256

        return sha256(uri.encode()).hexdigest()

    def load_accounts(self):
        entries = db.instance.entries
        for entry in entries:
            display_name = f"{entry.title} ({entry.username})"
            self.accounts[display_name] = entry
            self.hashes.append(self.get_digest(entry.url))
            self.list_widget.addItem(display_name)

        self.list_widget.setCurrentRow(0)

    def open_edit_account_window(self):
        from view.edit_account import EditAccountWindow

        selected_item = self.list_widget.currentItem()
        selected_account = self.accounts[selected_item.text()]
        self.edit_username_window = EditAccountWindow(selected_account.username)
        self.edit_username_window.closeEvent = self.update_accounts
        self.edit_username_window.show()

        # Center the window
        self.center_window(self.edit_username_window)

    def delete_account(self):
        # Create a dialog
        dialog = QMessageBox()
        dialog.setWindowTitle(String.DELETE_ENTRY_TITLE)
        dialog.setText(String.DELETE_ENTRY_BODY)
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        dialog.setIcon(QMessageBox.Warning)

        # Execute the dialog
        result = dialog.exec()

        if result == QMessageBox.Yes:
            selected_item = self.list_widget.currentItem()
            selected_account = self.accounts[selected_item.text()]
            db.instance.delete_entry(selected_account)
            db.instance.save()
            self.update_accounts()

    def update_accounts(self, *args):
        self.list_widget.clear()
        self.accounts = {}
        self.load_accounts()

    def keyPressEvent(self, event):
        # Check if the RETURN or ENTER key was pressed
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            # If the key has already been pressed once, check if the time elapsed is less than the threshold
            if self.key_pressed:
                # If the elapsed time is less than the threshold, copy the item's data to the clipboard
                if self.timer.elapsed() < 500:
                    item = self.list_widget.currentItem()
                    self.copy_otp_code(item)

                # Reset the flag and time
                self.reset_key_pressed()
            else:
                # If the key has not been pressed before, set the flag to indicate that it has been pressed once
                # and start the time
                self.key_pressed = True
                self.timer.start()

        super().keyPressEvent(event)

    def reset_key_pressed(self):
        self.key_pressed = False
        self.timer.invalidate()

    def center_window(self, window):
        window.move(
            self.frameGeometry().topLeft()
            + self.rect().center()
            - window.rect().center()
        )
