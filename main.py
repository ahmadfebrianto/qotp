import sys

import pyotp
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QMainWindow,
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

        btn_add_account = QPushButton("Add Account")
        btn_add_account.clicked.connect(self.open_add_account_window)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.list_widget)
        vlayout.addWidget(btn_add_account)

        widget.setLayout(vlayout)

    def open_add_account_window(self):
        from view.add_account import AddAccountWindow

        self.add_account_window = AddAccountWindow()
        self.add_account_window.data_ready.connect(self.add_account)
        self.add_account_window.show()

    def add_account(self, data):
        parsed_uri = self.parse_uri(data)
        title = parsed_uri.issuer
        username = parsed_uri.name
        password = parsed_uri.secret
        url = parsed_uri.provisioning_uri

        from model import db

        entry = db.instance.add_entry(
            db.instance.root_group, title, username, password, url=url
        )
        db.instance.save()

        self.update_accounts()

        # On double click, show the OTP code
        self.list_widget.itemDoubleClicked.connect(self.copy_otp_code)

    def parse_uri(self, data):
        parsed_uri = pyotp.parse_uri(data)
        return parsed_uri

    def copy_otp_code(self, item):
        parsed_uri = self.accounts[item.text()]
        otp_code = parsed_uri.now()
        QApplication.clipboard().setText(otp_code)
        self.show_notification("OTP code copied to clipboard")

    def show_notification(self, message):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setVisible(True)
        self.tray_icon.showMessage(
            "Authenticator", message, icon=QSystemTrayIcon.Information, msecs=1500
        )

    def load_accounts(self):
        entries = db.instance.entries
        for entry in entries:
            display_name = entry.title + " - " + entry.username
            self.list_widget.addItem(display_name)
            self.accounts[display_name] = entry

    def update_accounts(self):
        self.list_widget.clear()
        self.accounts = {}
        self.load_accounts()


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
