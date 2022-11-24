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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authenticator")
        self.setMinimumSize(600, 400)
        self.setup_ui()

        self.accounts = {}

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
        display_name = parsed_uri.issuer + " - " + parsed_uri.name
        self.list_widget.addItem(display_name)
        self.accounts[display_name] = parsed_uri

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


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.account = None

        self.window = MainWindow()
        self.window.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
