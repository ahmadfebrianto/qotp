from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from utils.config import config
from utils.constants import Constants
from utils.strings import String
from view.widget_file_dialog import FileDialogWidget


class ChooseActionWidget(QWidget):

    open_clicked = Signal()
    create_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(String.TITLE_CHOOSE_ACTION)
        # Open database button
        self.btn_open_db = QPushButton(String.TITLE_OPEN_DB)
        self.btn_open_db.setFixedWidth(Constants.BTN_WIDTH_WIDE)
        self.btn_open_db.clicked.connect(self.show_open_db_widget)
        # Create database button
        self.btn_create_db = QPushButton(String.TITLE_CREATE_DB)
        self.btn_create_db.setFixedWidth(Constants.BTN_WIDTH_WIDE)
        self.btn_create_db.clicked.connect(self.show_create_db_widget)
        # Layout
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.btn_open_db)
        self.vlayout.addWidget(self.btn_create_db)
        self.vlayout.setAlignment(Qt.AlignCenter)
        self.vlayout.setSpacing(Constants.LAYOUT_SPACING)
        self.setLayout(self.vlayout)

    def show_open_db_widget(self):
        db_path = FileDialogWidget().load_db()
        if not db_path:
            return

        config.set(String.CONFIG_SECTION_DB, String.CONFIG_KEY_DBPATH, db_path)
        self.open_clicked.emit()

    def show_create_db_widget(self):
        self.create_clicked.emit()
