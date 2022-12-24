from io import BytesIO

import qrcode
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from model.db import db
from utils.common import copy_to_clipboard
from utils.strings import String


class ExportAccountWindow(QMainWindow):
    def __init__(self, parent, entry):
        super().__init__(parent)
        self.entry = entry
        self.setFixedSize(300, 300)
        self.setWindowTitle(String.EXPORT_ACCOUNT_TITLE)
        self.setup_ui()

    def setup_ui(self):
        self.label_qr = QLabel()
        self.label_qr.setAlignment(Qt.AlignCenter)
        self.set_qr_label()

        self.btn_copy_secret = QPushButton(String.BTN_COPY_SECRET)
        self.btn_copy_secret.clicked.connect(self.copy_secret)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.label_qr)
        vlayout.addWidget(self.btn_copy_secret)

        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)

    def set_qr_label(self):
        uri = db.get_uri(self.entry)
        buf = BytesIO()
        img = qrcode.make(uri, box_size=5)
        img.save(buf, String.IMAGE_PNG)
        qt_pixmap = QPixmap()
        qt_pixmap.loadFromData(buf.getvalue(), String.IMAGE_PNG)
        self.label_qr.setPixmap(qt_pixmap)

    def copy_secret(self):
        secret = db.get_secret(self.entry)
        copy_to_clipboard(secret)
        self.close()
