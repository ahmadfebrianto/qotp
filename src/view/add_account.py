import io

from PySide6 import QtCore
from PySide6.QtCore import QBuffer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from utils.strings import String


class AddAccountWindow(QMainWindow):

    data_ready = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(String.ADD_ACCOUNT_TITLE)
        self.setMinimumSize(600, 400)
        self.setup_ui()

    def setup_ui(self):
        widget = QWidget()
        self.setCentralWidget(widget)

        btn_load_image = QPushButton(String.BTN_LOAD_IMAGE)
        btn_load_image.clicked.connect(self.open_file_dialog)

        btn_paste_image = QPushButton(String.BTN_PASTE_IMAGE)
        btn_paste_image.clicked.connect(self.paste_image)

        btn_read_qr_code = QPushButton(String.BTN_READ_QR_CODE)
        btn_read_qr_code.clicked.connect(self.read_qr_code)

        self.image_label = QLabel()

        # Horizontal layout for "Load image" and "Paste image" buttons
        hlayout = QHBoxLayout()
        hlayout.addWidget(btn_load_image)
        hlayout.addWidget(btn_paste_image)

        # Vertical layout for Image label and the buttons
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.image_label)
        # Center the image label
        vlayout.setAlignment(self.image_label, QtCore.Qt.AlignCenter)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(btn_read_qr_code)

        widget.setLayout(vlayout)

    def load_image(self, path):
        image = QImage(path)
        if image.isNull():
            return

        self.image_label.setPixmap(QPixmap.fromImage(image))

    def open_file_dialog(self):
        dialog = QFileDialog()
        dialog.setNameFilter(String.FILE_IMAGE_FILTER)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setDirectory(".")

        if dialog.exec():
            paths = dialog.selectedFiles()
            if paths:
                path = paths[0]
                self.load_image(path)

    def paste_image(self):
        # Get the image from the clipboard
        image = QApplication.clipboard().image()
        if image.isNull():
            return

        self.image_label.setPixmap(QPixmap.fromImage(image))
        QApplication.clipboard().clear()

    def read_qr_code(self):
        # Get the image from the label
        image = self.image_label.pixmap().toImage()

        if image.isNull():
            return

        from PIL import Image
        from pyzbar.pyzbar import decode

        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        image.save(buffer, String.IMAGE_PNG)
        data = decode(Image.open(io.BytesIO(buffer.data())))

        if not data:
            QMessageBox.warning(
                self,
                String.WARNING_DUPLICATE_TITLE,
                String.WARNING_NOT_QR_CODE,
            )
            return

        self.data_ready.emit(data[0].data.decode("utf-8"))
        self.close()
