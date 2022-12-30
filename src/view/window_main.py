from PySide6.QtWidgets import QMainWindow, QStackedWidget

from utils.strings import String
from view.widget_add_entry import AddEntryWidget
from view.widget_list_entry import ListEntryWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 150)
        self.setup_ui()
        self.show_entry_list()

    def setup_ui(self):
        self.list_entry_widget = ListEntryWidget()
        self.list_entry_widget.btn_add_entry.clicked.connect(self.show_add_entry_widget)
        self.list_entry_widget.otp_copied.connect(self.close)

        self.add_entry_widget = AddEntryWidget()
        self.add_entry_widget.entry_added.connect(self.show_entry_list)
        self.add_entry_widget.btn_cancel.clicked.connect(self.show_entry_list)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.list_entry_widget)
        self.stack.addWidget(self.add_entry_widget)
        self.setCentralWidget(self.stack)

    def show_entry_list(self):
        self.stack.setCurrentIndex(0)
        self.setWindowTitle(String.APP_NAME)
        self.list_entry_widget.update_entries()

    def show_add_entry_widget(self):
        self.stack.setCurrentIndex(1)
        self.setWindowTitle(String.TITLE_ADD_ENTRY)
