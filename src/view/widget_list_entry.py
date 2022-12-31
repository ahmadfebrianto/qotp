import re
from time import sleep

from PySide6.QtCore import QElapsedTimer, Qt, Signal
from PySide6.QtWidgets import (
    QListWidget,
    QMenu,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from model.db import db
from utils.common import copy_to_clipboard, show_notification
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
        self.timer = QElapsedTimer()

    def setup_ui(self):
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.copy_otp_code)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_menu)
        self.list_widget.setStyleSheet("QListWidget::item { padding: 10px; }")
        # Add entry button
        self.btn_add_entry = QPushButton(String.BTN_ADD_ENTRY)

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
        menu.exec(self.list_widget.mapToGlobal(position))

    def copy_otp_code(self, item=None):
        if not item:
            item = self.list_widget.currentItem()
        otp_code = db.get_otp_code(item.text())
        copy_to_clipboard(otp_code)
        show_notification(String.APP_NAME, String.NOTIF_COPY_SUCCESS)
        sleep(1)
        self.otp_copied.emit()

    def on_menu_export_clicked(self):
        chosen_entry = self.list_widget.currentItem().text()
        self.export_clicked.emit(chosen_entry)

    def on_menu_edit_clicked(self):
        selected_entry = self.list_widget.currentItem().text()
        username = re.search(r"\((.*)\)", selected_entry).group(1)
        self.edit_clicked.emit(username)

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
                if self.timer.elapsed() < Constants.DOUBLE_TAP_INTERVAL:
                    item = self.list_widget.currentItem()
                    self.copy_otp_code(item)
                # Reset the flag and time
                self.reset_key_pressed()
            else:
                # If the key has not been pressed before,
                # set the flag to indicate that it has been pressed once
                # and start the time
                self.key_pressed = True
                self.timer.start()

    def reset_key_pressed(self):
        self.key_pressed = False
        self.timer.invalidate()
