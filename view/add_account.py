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
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AddAccountWindow(QMainWindow):

    data_ready = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Account")
        self.setMinimumSize(600, 400)
        self.setup_ui()

    def setup_ui(self):
        widget = QWidget()
        self.setCentralWidget(widget)

        btn_load_image = QPushButton("Load Image")
        btn_load_image.clicked.connect(self.open_file_dialog)

        btn_paste_image = QPushButton("Paste Image")
        btn_paste_image.clicked.connect(self.paste_image)

        btn_read_qr_code = QPushButton("Read QR Code")
        btn_read_qr_code.clicked.connect(self.read_qr_code)

        self.image_label = QLabel()

        # Horizontal layout for "Load image" and "Paste image" buttons
        hlayout = QHBoxLayout()
        hlayout.addWidget(btn_load_image)
        hlayout.addWidget(btn_paste_image)

        # Vertical layout for Image label and the buttons
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.image_label)
        vlayout.addLayout(hlayout)
        vlayout.addWidget(btn_read_qr_code)

        widget.setLayout(vlayout)

    def load_image(self, path):
        image = QImage(path)
        if image.isNull():
            print("Cannot load image")
            return

        self.image_label.setPixmap(QPixmap.fromImage(image))

    def open_file_dialog(self):
        dialog = QFileDialog()
        dialog.setNameFilter("Images (*.png *.jpg)")
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
            print("Cannot load image")
            return

        self.image_label.setPixmap(QPixmap.fromImage(image))

    def read_qr_code(self):
        # Get the image from the label
        image = self.image_label.pixmap().toImage()

        if image.isNull():
            print("Cannot load image")
            return

        from PIL import Image
        from pyzbar.pyzbar import decode

        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        image.save(buffer, "PNG")
        data = decode(Image.open(io.BytesIO(buffer.data())))

        if not data:
            print("No QR code found")
            return

        self.data_ready.emit(data[0].data.decode("utf-8"))
        # app = QApplication.instance()
        # app.clipboard().setText(data[0].data.decode("utf-8"))

        self.close()
