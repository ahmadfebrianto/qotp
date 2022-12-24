import io

from PIL import Image
from PySide6 import QtCore
from PySide6.QtCore import QBuffer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from pyzbar.pyzbar import decode

from model.db import db
from utils.strings import String


class AddAccountWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(String.ADD_ACCOUNT_TITLE)
        self.setMinimumSize(600, 400)
        self.setup_ui()

    def setup_ui(self):
        # Load image button
        btn_load_image = QPushButton(String.BTN_LOAD_IMAGE)
        btn_load_image.clicked.connect(self.load_qr_image)
        # Paste image button
        btn_paste_image = QPushButton(String.BTN_PASTE_IMAGE)
        btn_paste_image.clicked.connect(self.paste_qr_image)
        # Read QR code button
        btn_read_qr_code = QPushButton(String.BTN_READ_QR_CODE)
        btn_read_qr_code.clicked.connect(self.read_qr_code)
        # Image label (placeholder for the image)
        self.image_label = QLabel()
        # Horizontal layout for "Load image" and "Paste image" buttons
        hlayout = QHBoxLayout()
        hlayout.addWidget(btn_load_image)
        hlayout.addWidget(btn_paste_image)
        # Vertical layout for Image label and hlayout (the buttons)
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.image_label)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(btn_read_qr_code)
        # Center the image
        vlayout.setAlignment(self.image_label, QtCore.Qt.AlignCenter)
        # Set layout
        self.setLayout(vlayout)

    def set_qr_image(self, path):
        image = QImage(path)
        if not self.ensure_image_size(image):
            self.show_warning(String.WARNING_INVALID_IMAGE_SIZE)
            return

        self.image_label.setPixmap(QPixmap.fromImage(image))

    def load_qr_image(self):
        dialog = QFileDialog()
        dialog.setNameFilter(String.FILE_IMAGE_FILTER)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setDirectory(".")

        if dialog.exec():
            paths = dialog.selectedFiles()
            if paths:
                path = paths[0]
                self.set_qr_image(path)

    def paste_qr_image(self):
        # Get the image from the clipboard
        image = QApplication.clipboard().image()
        if image.isNull():
            return

        # Ensure the image size is not too large
        if not self.ensure_image_size(image):
            self.show_warning(String.WARNING_INVALID_IMAGE_SIZE)
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
            self.show_warning(String.WARNING_INVALID_QR)
            return

        uri = data[0].data.decode(String.UTF_8)
        if db.exists(uri):
            self.show_warning(String.WARNING_DUPLICATE_ENTRY)
            return

        db.add_entry(uri)
        self.close()

    def ensure_image_size(self, image):
        # Limit image size to 1MB
        MAX_LIMIT = 1024 * 1024
        if image.sizeInBytes() > MAX_LIMIT:
            return False

        return True

    def show_warning(self, warning):
        if warning == String.WARNING_INVALID_IMAGE_SIZE:
            QMessageBox.warning(
                self,
                String.WARNING_INVALID_IMAGE_SIZE,
                String.WARNING_INVALID_IMAGE_SIZE_BODY,
            )

        elif warning == String.WARNING_INVALID_QR:
            QMessageBox.warning(
                self,
                String.WARNING_INVALID_QR,
                String.WARNING_INVALID_QR_BODY,
            )

        elif warning == String.WARNING_DUPLICATE_ENTRY:
            QMessageBox.warning(
                self,
                String.WARNING_DUPLICATE_ENTRY,
                String.WARNING_DUPLICATE_ENTRY_BODY,
            )
