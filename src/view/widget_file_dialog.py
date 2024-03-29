import os

from PySide6.QtWidgets import QFileDialog

from utils.strings import String


class FileDialogWidget(QFileDialog):
    def load_qr(self):
        self.setWindowTitle(String.TITLE_LOAD_IMAGE)
        self.setFileMode(QFileDialog.ExistingFile)
        self.setNameFilter(String.FILTER_IMAGE)
        self.setDirectory(os.getenv(String.DIR_HOME))

        if self.exec() == QFileDialog.Accepted:
            return self.selectedFiles()[0]
        return None

    def choose_db_location(self):
        self.setWindowTitle(String.TITLE_CHOOSE_DB_LOCATION)
        self.setFileMode(QFileDialog.Directory)
        self.setDirectory(os.getenv(String.DIR_HOME))
        self.setOptions(QFileDialog.ShowDirsOnly)

        if self.exec() == QFileDialog.Accepted:
            return self.selectedFiles()[0]
        return None

    def load_db(self):
        self.setWindowTitle(String.TITLE_LOAD_DB)
        self.setFileMode(QFileDialog.ExistingFile)
        self.setNameFilter(String.FILTER_DB)
        self.setDirectory(os.getenv(String.DIR_HOME))

        if self.exec() == QFileDialog.Accepted:
            return self.selectedFiles()[0]
        return None
