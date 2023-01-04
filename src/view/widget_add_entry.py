import io

from PIL import Image
from PySide6.QtCore import QBuffer, Qt, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from pyzbar.pyzbar import decode

from model.db import db
from utils.constants import Constants
from utils.strings import String
from view.widget_file_dialog import FileDialogWidget


class AddEntryWidget(QWidget):

    entry_added = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(String.TITLE_ADD_ENTRY)
        self.setup_ui()

    def setup_ui(self):
        # Load image button
        self.btn_load_image = QPushButton(String.BTN_LOAD_IMAGE)
        self.btn_load_image.clicked.connect(self.load_qr_image)
        # Paste image button
        self.btn_paste_image = QPushButton(String.BTN_PASTE_IMAGE)
        self.btn_paste_image.clicked.connect(self.paste_qr_image)
        # Cancel Button
        self.btn_cancel = QPushButton(String.BTN_CANCEL)
        # self.btn_cancel.clicked.connect(self.close)
        # Read QR code button
        self.btn_read_qr_code = QPushButton(String.BTN_READ_QR_CODE)
        self.btn_read_qr_code.clicked.connect(self.read_qr_code)
        # Image label (placeholder for the image)
        self.image_label = QLabel()
        # Horizontal layout for "Load image" and "Paste image" buttons
        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(self.btn_load_image)
        self.hlayout.addWidget(self.btn_paste_image)
        # Vertical layout for "Cancel" and "Read QR code" buttons
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.btn_read_qr_code)
        self.vlayout.addWidget(self.btn_cancel)
        # Vertical layout for Image label and self.hlayout (the buttons)
        self.main_vlayout = QVBoxLayout()
        self.main_vlayout.addWidget(self.image_label)
        self.main_vlayout.addLayout(self.hlayout)
        self.main_vlayout.addLayout(self.vlayout)
        # Center the image
        self.main_vlayout.setAlignment(self.image_label, Qt.AlignCenter)
        # Set layout
        self.setLayout(self.main_vlayout)

    def set_qr_image(self, path):
        image = QImage(path)
        if not self.ensure_image_size(image):
            self.show_warning(String.WARN_INVALID_IMAGE_SIZE)
            return

        self.image_label.setPixmap(QPixmap.fromImage(image))

    def load_qr_image(self):
        qr = FileDialogWidget().load_qr()
        if qr:
            self.set_qr_image(qr)

    def paste_qr_image(self):
        # Get the image from the clipboard
        image = QApplication.clipboard().image()
        if image.isNull():
            return

        # Ensure the image size is not too large
        if not self.ensure_image_size(image):
            self.show_warning(String.WARN_INVALID_IMAGE_SIZE)
            return

        self.image_label.setPixmap(QPixmap.fromImage(image))
        QApplication.clipboard().clear()

    def read_qr_code(self):
        # Get the image from the label
        image = self.image_label.pixmap().toImage()
        if image.isNull():
            return

        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        image.save(buffer, String.IMAGE_PNG)
        data = decode(Image.open(io.BytesIO(buffer.data())))
        if not data:
            self.show_warning(String.WARN_INVALID_QR)
            return

        uri = data[0].data.decode(String.UTF_8)
        if db.entry_exists(uri):
            self.show_warning(String.WARN_DUPLICATE_ENTRY)
            return

        db.add_entry(uri)
        self.image_label.clear()
        self.entry_added.emit()

    def ensure_image_size(self, image):
        if image.sizeInBytes() > Constants.MAX_IMAGE_SIZE:
            return False
        return True

    def show_warning(self, warning):
        if warning == String.WARN_INVALID_IMAGE_SIZE:
            QMessageBox.warning(
                self,
                String.WARN_INVALID_IMAGE_SIZE,
                String.WARN_INVALID_IMAGE_SIZE_BODY,
            )

        elif warning == String.WARN_INVALID_QR:
            QMessageBox.warning(
                self,
                String.WARN_INVALID_QR,
                String.WARN_INVALID_QR_BODY,
            )

        elif warning == String.WARN_DUPLICATE_ENTRY:
            QMessageBox.warning(
                self,
                String.WARN_DUPLICATE_ENTRY,
                String.WARN_DUPLICATE_ENTRY_BODY,
            )
