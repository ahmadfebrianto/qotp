import re
from time import sleep

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
from utils.common import copy_to_clipboard, show_notification
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
        self.add_account_window.closed.connect(self.load_accounts)
        self.add_account_window.show()

    def open_export_account_window(self):
        from view.export_account import ExportAccountWindow

        chosen_entry = self.list_widget.currentItem().text()
        self.export_account_window = ExportAccountWindow(self, chosen_entry)
        self.export_account_window.show()

    def copy_otp_code(self, item=None):
        if not item:
            item = self.list_widget.currentItem()
        otp_code = db.get_otp_code(item.text())
        copy_to_clipboard(otp_code)

        show_notification(String.APP_NAME, String.NOTIF_COPY_SUCCESS)
        sleep(1)
        self.close()

    def load_accounts(self):
        entries = db.entries
        for entry in entries:
            display_name = f"{entry.title} ({entry.username})"
            self.accounts[display_name] = entry
            self.list_widget.addItem(display_name)

        self.list_widget.setCurrentRow(0)

    def open_edit_account_window(self):
        from view.edit_account import EditAccountWindow

        selected_entry = self.list_widget.currentItem().text()
        username = re.search(r"\((.*)\)", selected_entry).group(1)
        self.edit_username_window = EditAccountWindow(username)
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

        result = dialog.exec()
        if result == QMessageBox.Yes:
            selected_item = self.list_widget.currentItem()
            db.delete_entry(selected_item.text())
            self.update_accounts()

    def update_accounts(self, *args):
        self.list_widget.clear()
        self.accounts = {}
        self.load_accounts()

        # Set the last item as the current item
        self.list_widget.setCurrentRow(self.list_widget.count() - 1)

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
