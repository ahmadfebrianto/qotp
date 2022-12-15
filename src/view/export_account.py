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

from utils.strings import String


class ExportAccountWindow(QMainWindow):
    def __init__(self, parent, account):
        super().__init__(parent)
        self.account = account
        self.setFixedSize(300, 300)
        self.setWindowTitle(String.EXPORT_ACCOUNT_TITLE)
        self.setup_ui()

    def setup_ui(self):
        self.label_qr = QLabel()
        self.label_qr.setAlignment(Qt.AlignCenter)
        self.set_qr_label(self.account.url)

        self.btn_copy_secret = QPushButton(String.BTN_COPY_SECRET)
        self.btn_copy_secret.clicked.connect(self.copy_secret)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.label_qr)
        vlayout.addWidget(self.btn_copy_secret)

        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)

    def set_qr_label(self, text):
        buf = BytesIO()
        img = qrcode.make(text, box_size=5)
        img.save(buf, String.IMAGE_PNG)
        qt_pixmap = QPixmap()
        qt_pixmap.loadFromData(buf.getvalue(), String.IMAGE_PNG)
        self.label_qr.setPixmap(qt_pixmap)

    def copy_secret(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.account.password)
        self.close()
