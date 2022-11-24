import sys

from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authenticator")
        self.setMinimumSize(600, 400)
        self.setup_ui()

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
        pass


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.account = None

        self.window = MainWindow()
        self.window.show()


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())
