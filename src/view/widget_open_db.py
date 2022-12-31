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
        # Database path label and input
        self.label_db_path = QLabel(String.LABEL_DB_PATH)
        self.label_db_path.setFixedWidth(Constants.LABEL_MAX_WIDTH)
        self.input_db_path = QLineEdit()
        self.input_db_path.setReadOnly(True)
        self.input_db_path.setPlaceholderText(String.PHOLDER_DB_LOCATION)
        self.input_db_path.setText(
            config[String.CONFIG_SECTION_DB][String.CONFIG_KEY_DBPATH]
        )
        self.btn_open_db = QPushButton(String.BTN_DOTS)
        self.btn_open_db.clicked.connect(self.open_db_location_dialog)
        self.hlayout_db_path = QHBoxLayout()
        self.hlayout_db_path.addWidget(self.label_db_path)
        self.hlayout_db_path.addWidget(self.input_db_path)
        self.hlayout_db_path.addWidget(self.btn_open_db)
        # Database password label and input
        self.label_db_password = QLabel(String.LABEL_DB_PASSWORD)
        self.label_db_password.setFixedWidth(Constants.LABEL_MAX_WIDTH)
        self.input_db_password = QLineEdit()
        self.input_db_password.setEchoMode(QLineEdit.Password)
        self.input_db_password.returnPressed.connect(self.open_db)
        self.hlayout_db_password = QHBoxLayout()
        self.hlayout_db_password.addWidget(self.label_db_password)
        self.hlayout_db_password.addWidget(self.input_db_password)
        # Cancel and open database buttons
        self.cancel_btn = QPushButton(String.BTN_CANCEL)
        self.cancel_btn.setFixedWidth(Constants.BTN_NORMAL_MIN_WIDTH)
        self.cancel_btn.clicked.connect(self.canceled.emit)
        self.open_db_btn = QPushButton(String.BTN_OPEN_DB)
        self.open_db_btn.setFixedWidth(Constants.BTN_NORMAL_MIN_WIDTH)
        self.open_db_btn.clicked.connect(self.open_db)
        self.hlayout_buttons = QHBoxLayout()
        self.hlayout_buttons.addWidget(self.cancel_btn)
        self.hlayout_buttons.addWidget(self.open_db_btn)
        self.hlayout_buttons.setSpacing(Constants.LAYOUT_SPACING)
        self.hlayout_buttons.setAlignment(Qt.AlignRight)
        # Main layout
        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout_db_path)
        self.vlayout.addLayout(self.hlayout_db_password)
        self.vlayout.addLayout(self.hlayout_buttons)
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
            self.input_db_password.setStyleSheet(
                "QLineEdit { border: 1px solid tomato; padding: 2px;}"
            )
            self.input_db_password.setToolTip(str(e))
            return

        config.set(String.CONFIG_SECTION_DB, String.CONFIG_KEY_DBPATH, label_db_path)
        config.save()
        self.db_opened.emit()
