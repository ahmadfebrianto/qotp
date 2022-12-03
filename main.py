import sys

import pyotp
from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
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
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)

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

        db.instance.add_entry(
            db.instance.root_group, title, username, password, url=url
        )
        db.instance.save()

        self.update_accounts()

    def parse_uri(self, data):
        parsed_uri = pyotp.parse_uri(data)
        return parsed_uri

    def copy_otp_code(self, item):
        widget = self.list_widget.itemWidget(item)
        label = widget.findChild(QLabel)
        clicked_account = self.accounts[label.text()]
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
            app_icon="icon.ico",
            timeout=1,
        )

    def load_accounts(self):
        entries = db.instance.entries
        for entry in entries:

            display_name = f"{entry.title} ({entry.username})"
            label_account = QLabel(display_name)
            self.accounts[display_name] = entry

            button_edit = QPushButton("Edit")
            button_edit.setObjectName("button_edit")
            button_edit.hide()
            button_edit.clicked.connect(self.open_edit_account_window)

            button_delete = QPushButton("Delete")
            button_delete.setObjectName("button_delete")
            button_delete.hide()
            button_delete.clicked.connect(self.delete_account)

            hbutton_layout = QHBoxLayout()
            hbutton_layout.addStretch()
            hbutton_layout.addWidget(button_edit)
            hbutton_layout.addWidget(button_delete)

            hlayout = QHBoxLayout()
            hlayout.addWidget(label_account)
            hlayout.addLayout(hbutton_layout)

            widget = QWidget()
            widget.setLayout(hlayout)

            widget_item = QListWidgetItem()
            widget_item.setSizeHint(widget.sizeHint())

            self.list_widget.addItem(widget_item)
            self.list_widget.setItemWidget(widget_item, widget)

        self.list_widget.setCurrentRow(0)

    def open_edit_account_window(self):
        pass

    def delete_account(self):
        pass

    def update_accounts(self):
        self.list_widget.clear()
        self.accounts = {}
        self.load_accounts()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.copy_otp_code(self.list_widget.currentItem())

    def on_selection_changed(self):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            widget = self.list_widget.itemWidget(item)
            widget.findChild(QPushButton, "button_edit").hide()
            widget.findChild(QPushButton, "button_delete").hide()

        item = self.list_widget.currentItem()
        widget = self.list_widget.itemWidget(item)
        widget.findChild(QPushButton, "button_edit").show()
        widget.findChild(QPushButton, "button_delete").show()


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
