from io import BytesIO

import qrcode
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

from model.db import db
from utils.common import load_stylesheet
from utils.constants import Constants
from utils.strings import String


class ExportEntryWidget(QWidget):
    def __init__(self, entry):
        super().__init__()
        self.entry = entry
        self.setWindowTitle(String.TITLE_EXPORT_ENTRY)
        self.setup_ui()
        self.setStyleSheet(load_stylesheet())

    def setup_ui(self):
        # Set window frameless
        self.setWindowFlags(Qt.FramelessWindowHint)
        # QR code label (image placeholder)
        self.label_qr = QLabel()
        self.label_qr.setAlignment(Qt.AlignCenter)
        self.set_qr_label()
        # Copy secret button
        self.btn_copy_secret = QPushButton(String.BTN_COPY_SECRET)
        self.btn_copy_secret.clicked.connect(self.copy_secret)
        # Layout setup
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.label_qr)
        self.vlayout.addWidget(self.btn_copy_secret)
        self.setLayout(self.vlayout)

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
        QApplication.clipboard().setText(secret)
        self.close()

    def show(self):
        super().show()
        self.setFixedSize(self.size())

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Escape:
            self.close()
