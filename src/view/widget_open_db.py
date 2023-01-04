from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from model.db import db
from utils.config import config
from utils.constants import Constants
from utils.strings import String
from view.widget_file_dialog import FileDialogWidget


class OpenDBWidget(QWidget):

    db_opened = Signal()
    canceled = Signal()

    def __init__(self):
        super().__init__()
        config.read()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(String.TITLE_OPEN_DB)
        # Database path input
        self.input_db_path = QLineEdit()
        self.input_db_path.setReadOnly(True)
        self.input_db_path.setPlaceholderText(String.PHOLDER_DB_LOCATION)
        self.input_db_path.returnPressed.connect(self.open_db_location_dialog)
        self.btn_open_file = QPushButton(String.BTN_DOTS)
        self.btn_open_file.setFixedWidth(Constants.BTN_WIDTH_DOTS)
        self.btn_open_file.clicked.connect(self.open_db_location_dialog)
        self.hlayout_db_path = QHBoxLayout()
        self.hlayout_db_path.addWidget(self.input_db_path)
        self.hlayout_db_path.addWidget(self.btn_open_file)
        # Database password label and input
        self.input_db_password = QLineEdit()
        self.input_db_password.setEchoMode(QLineEdit.Password)
        self.input_db_password.setPlaceholderText(String.PHOLDER_DB_PASSWORD)
        self.input_db_password.returnPressed.connect(self.open_db)
        # Cancel and open database buttons
        self.btn_open_db = QPushButton(String.BTN_OPEN_DB)
        self.btn_open_db.setFixedWidth(Constants.BTN_WIDTH_WIDE)
        self.btn_open_db.clicked.connect(self.open_db)
        self.btn_cancel = QPushButton(String.BTN_CANCEL)
        self.btn_cancel.setFixedWidth(Constants.BTN_WIDTH_WIDE)
        self.btn_cancel.clicked.connect(self.canceled.emit)
        self.vlayout_buttons = QVBoxLayout()
        self.vlayout_buttons.addWidget(self.btn_open_db)
        self.vlayout_buttons.addWidget(self.btn_cancel)
        self.vlayout_buttons.setSpacing(Constants.LAYOUT_SPACING)
        self.vlayout_buttons.setAlignment(Qt.AlignCenter)
        # Main layout
        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout_db_path)
        self.vlayout.addWidget(self.input_db_password)
        self.vlayout.addLayout(self.vlayout_buttons)
        self.vlayout.setSpacing(Constants.LAYOUT_SPACING)
        self.setLayout(self.vlayout)

    def open_db_location_dialog(self):
        db = FileDialogWidget().load_db()
        if db:
            self.input_db_path.setText(db)

    def open_db(self):
        label_db_path = self.input_db_path.text()
        db_password = self.input_db_password.text()

        try:
            db.open(label_db_path, db_password)
        except Exception as e:
            self.input_db_password.setProperty("cssClass", "error")
            self.input_db_password.style().polish(self.input_db_password)
            return

        config.set(String.CONFIG_SECTION_DB, String.CONFIG_KEY_DBPATH, label_db_path)
        config.save()
        self.db_opened.emit()
