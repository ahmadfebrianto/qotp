from PySide6.QtWidgets import QMainWindow, QStackedWidget

from utils.common import load_stylesheet
from utils.constants import Constants
from utils.strings import String
from view.widget_add_entry import AddEntryWidget
from view.widget_edit_entry import EditEntryWidget
from view.widget_export_entry import ExportEntryWidget
from view.widget_list_entry import ListEntryWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setMinimumSize(*Constants.WINDOW_MAIN_SIZE)
        self.setup_ui()
        self.setStyleSheet(load_stylesheet())
        self.show_entry_list()
        self.setFixedSize(self.size())

    def setup_ui(self):
        # List entry widget
        self.list_entry_widget = ListEntryWidget()
        self.list_entry_widget.btn_add_entry.clicked.connect(self.show_add_entry_widget)
        self.list_entry_widget.otp_copied.connect(self.close)
        self.list_entry_widget.edit_clicked.connect(self.show_edit_entry_widget)
        self.list_entry_widget.export_clicked.connect(self.show_export_entry_widget)
        # Add entry widget
        self.add_entry_widget = AddEntryWidget()
        self.add_entry_widget.entry_added.connect(self.show_entry_list)
        self.add_entry_widget.btn_cancel.clicked.connect(self.show_entry_list)
        # Stacked widget
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

    def show_edit_entry_widget(self, username):
        self.edit_entry_widget = EditEntryWidget(username)
        self.edit_entry_widget.edit_done.connect(self.show_entry_list)
        self.edit_entry_widget.show()
        self.center_window(self.edit_entry_widget)

    def show_export_entry_widget(self, entry):
        self.export_entry_widget = ExportEntryWidget(entry)
        self.export_entry_widget.show()

    def closeEvent(self, event):
        self.export_entry_widget = None
        self.edit_entry_widget = None
        event.accept()

    def center_window(self, window):
        window.move(
            self.frameGeometry().topLeft()
            + self.rect().center()
            - window.rect().center()
        )
