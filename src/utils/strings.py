import os

from .common import get_config_path


class String:
    APP_NAME = "QOTP"
    APP_NAME_LOWER = APP_NAME.lower()
    APP_DB_EXT = ".kdbx"

    # File: view/main_window.py
    BUTTON_ADD_ACCOUNT = "Add Account"
    CTX_MENU_COPY = "Copy OTP code"
    CTX_MENU_EXPORT = "Export entry"
    CTX_MENU_EDIT = "Edit entry"
    CTX_MENU_DELETE = "Delete entry"

    WARNING_DUPLICATE_ENTRY = "Duplicate entry"
    WARNING_DUPLICATE_ENTRY_BODY = "This entry already exists in your database"

    NOTIF_COPY_SUCCESS = "OTP code copied to clipboard"

    DELETE_ENTRY_TITLE = "Delete entry"
    DELETE_ENTRY_BODY = "Are you sure you want to delete this entry?"

    # File: view/add_account.py
    ADD_ACCOUNT_TITLE = "Add Account"

    BTN_LOAD_IMAGE = "Load Image"
    BTN_PASTE_IMAGE = "Paste Image"
    BTN_READ_QR_CODE = "Read QR Code"

    FILE_IMAGE_FILTER = "Image Files (*.png *.jpg *.bmp)"
    IMAGE_PNG = "PNG"

    WARNING_INVALID_QR = "Invalid QR Code"
    WARNING_INVALID_QR_BODY = "This is not a valid QR code."

    WARNING_INVALID_IMAGE_SIZE = "Invalid image size"
    WARNING_INVALID_IMAGE_SIZE_BODY = "Image size is too large."

    # File: view/edit_account.py
    EDIT_ACCOUNT_TITLE = "Edit Account"
    PH_NEW_USERNAME = "New username"
    BTN_SAVE_USERNAME = "Save"

    # File: view/create_db.py
    CREATE_DB_TITLE = "Create Database"
    LABEL_DB_NAME = "Database name"
    LABEL_DB_LOCATION = "Database location"
    PH_DB_LOCATION = "Select location"
    LABEL_DB_PASSWORD = "Database password"
    LABEL_DB_PASSWORD_CONFIRM = "Confirm password"

    BTN_DIALOG = "..."
    DB_DIALOG_TITLE = "Select a location for the database"
    BTN_CREATE_DB = "Create database"

    # File: view/export_account.py
    EXPORT_ACCOUNT_TITLE = "Export Account"
    BTN_COPY_SECRET = "Copy secret"

    # File: utils/config.py
    APP_CONFIG_NAME = APP_NAME_LOWER + ".conf"
    APP_CONFIG_PATH = get_config_path(APP_NAME_LOWER, APP_CONFIG_NAME)
    DB_PATH_KEY = "db_path"

    # Etc
    UTF_8 = "utf-8"

    @classmethod
    def get_db_path(cls, dir, name):
        return os.path.join(dir, name + cls.APP_DB_EXT)