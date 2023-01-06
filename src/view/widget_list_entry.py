from PySide6.QtCore import QElapsedTimer, Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QMenu,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from model.db import db
from utils.common import load_stylesheet
from utils.constants import Constants
from utils.strings import String


class ListEntryWidget(QWidget):

    otp_copied = Signal()
    edit_clicked = Signal(str)
    export_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(String.APP_NAME)
        self.setup_ui()
        self.key_pressed = False
        self.elapsed_timer = QElapsedTimer()
        self.timeout_timer = QTimer()

    def setup_ui(self):
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.copy_otp_code)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_menu)
        # Add entry button
        self.btn_add_entry = QPushButton(String.BTN_ADD_ENTRY)
        # Layout
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(self.list_widget)
        self.vlayout.addWidget(self.btn_add_entry)
        self.setLayout(self.vlayout)

    def show_menu(self, position):
        menu = QMenu()
        menu.addAction(String.CTX_MENU_COPY, self.copy_otp_code)
        menu.addAction(String.CTX_MENU_EXPORT, self.on_menu_export_clicked)
        menu.addAction(String.CTX_MENU_EDIT, self.on_menu_edit_clicked)
        menu.addAction(String.CTX_MENU_DELETE, self.delete_entry)
        menu.setStyleSheet(load_stylesheet())
        menu.exec(self.list_widget.mapToGlobal(position))

    def copy_otp_code(self, item=None):
        if not item:
            item = self.list_widget.currentItem()
        text = item.text()
        otp_code = db.get_otp_code(text)
        QApplication.clipboard().setText(otp_code)
        self.notify(item)

    def on_menu_export_clicked(self):
        chosen_entry = self.list_widget.currentItem().text()
        self.export_clicked.emit(chosen_entry)

    def on_menu_edit_clicked(self):
        selected_entry = self.list_widget.currentItem().text()
        self.edit_clicked.emit(selected_entry)

    def delete_entry(self):
        # Create a dialog
        dialog = QMessageBox()
        dialog.setWindowTitle(String.TITLE_DELETE_ENTRY)
        dialog.setText(String.BODY_DELETE_ENTRY)
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        dialog.setIcon(QMessageBox.Warning)

        result = dialog.exec()
        if result == QMessageBox.Yes:
            selected_item = self.list_widget.currentItem()
            db.delete_entry(selected_item.text())
            self.update_entries()

    def load_entries(self):
        if not db.entries:
            return
        for entry in db.entries:
            entry_display = f"{entry.title} ({entry.username})"
            self.list_widget.addItem(entry_display)

    def update_entries(self, *args):
        currentRow = self.list_widget.currentRow()
        previousCount = self.list_widget.count()
        self.list_widget.clear()
        self.load_entries()

        if self.list_widget.count() > previousCount:
            self.list_widget.setCurrentRow(previousCount)
        elif self.list_widget.count() < previousCount:
            self.list_widget.setCurrentRow(currentRow - 1)
        else:
            self.list_widget.setCurrentRow(currentRow)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        # Check if the RETURN or ENTER key was pressed
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # If the key has already been pressed once,
            # check if the time elapsed is less than the threshold
            if self.key_pressed:
                # If the elapsed time is less than the threshold,
                # copy the item's data to the clipboard
                if self.elapsed_timer.elapsed() < Constants.DOUBLE_TAP_INTERVAL:
                    item = self.list_widget.currentItem()
                    self.copy_otp_code(item)
                # Reset the flag and time
                self.reset_key_pressed()
            else:
                # If the key has not been pressed before,
                # set the flag to indicate that it has been pressed once
                # and start the time
                self.key_pressed = True
                self.elapsed_timer.start()

    def reset_key_pressed(self):
        self.key_pressed = False
        self.elapsed_timer.invalidate()

    def notify(self, widget):
        def update_text():
            widget.setText(original_text)
            self.timeout_timer.singleShot(
                Constants.NOTIF_DURATION, self.otp_copied.emit
            )

        original_text = widget.text()
        widget.setText(String.NOTIF_OTP_COPIED)
        self.timeout_timer.singleShot(Constants.NOTIF_DURATION, update_text)
