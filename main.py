import sys

import pyotp
from PySide6 import QtCore
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from model import db
from utils import config
from view.create_db import CreateDBWindow
from view.open_db import OpenDBWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OTPY")
        self.setMinimumSize(600, 400)
        self.setup_ui()
        self.accounts = {}
        self.load_accounts()

    def setup_ui(self):
        widget = QWidget()
        self.setCentralWidget(widget)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.copy_otp_code)
        self.list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_menu)
        self.list_widget.setStyleSheet("QListWidget::item { padding: 10px; }")

        btn_add_account = QPushButton("Add Account")
        btn_add_account.clicked.connect(self.open_add_account_window)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.list_widget)
        vlayout.addWidget(btn_add_account)

        widget.setLayout(vlayout)

    def show_menu(self, position):
        from PySide6.QtWidgets import QMenu

        menu = QMenu()
        menu.addAction("Edit entry", self.open_edit_account_window)
        menu.addAction("Delete entry", self.delete_account)
        menu.exec(self.list_widget.mapToGlobal(position))

    def open_add_account_window(self):
        from view.add_account import AddAccountWindow

        self.add_account_window = AddAccountWindow()
        self.add_account_window.data_ready.connect(self.add_account)
        self.add_account_window.show()

        # Center the window
        self.center_window(self.add_account_window)

    def add_account(self, data):
        parsed_uri = self.parse_uri(data)
        title = parsed_uri.issuer
        username = parsed_uri.name
        password = parsed_uri.secret
        url = parsed_uri.provisioning_uri

        from model import db

        db.instance.add_entry(
            db.instance.root_group, title, username, password, url=url
        )
        db.instance.save()

        self.update_accounts()

    def parse_uri(self, data):
        parsed_uri = pyotp.parse_uri(data)
        return parsed_uri

    def copy_otp_code(self, item):
        clicked_account = self.accounts[item.text()]
        parsed_uri = pyotp.parse_uri(clicked_account.url)
        otp_code = parsed_uri.now()
        QApplication.clipboard().setText(otp_code)
        self.show_notification("OTP code copied to clipboard")

    def show_notification(self, message):
        import plyer

        plyer.notification.notify(
            title="OTPY",
            message=message,
            app_name="OTPY",
            timeout=1,
        )

    def load_accounts(self):
        entries = db.instance.entries
        for entry in entries:

            display_name = f"{entry.title} ({entry.username})"
            self.accounts[display_name] = entry
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

    def save_changes(self):
        pass

    def delete_account(self):
        # Create a dialog
        dialog = QMessageBox()
        dialog.setWindowTitle("Delete entry")
        dialog.setText("Are you sure you want to delete this entry?")
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
        if event.key() == QtCore.Qt.Key_Return:
            self.copy_otp_code(self.list_widget.currentItem())

    def center_window(self, window):
        window.move(
            self.frameGeometry().topLeft()
            + self.rect().center()
            - window.rect().center()
        )


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        if not config.is_present:
            self.create_db_window = CreateDBWindow()
            self.create_db_window.data_ready.connect(self.open_main_window)
            self.create_db_window.show()

        else:
            self.open_db_window = OpenDBWindow()
            self.open_db_window.data_ready.connect(self.open_main_window)
            self.open_db_window.show()

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
