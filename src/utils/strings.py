import os

from .common import get_config_path


class String:
    APP_NAME = "QOTP"
    APP_NAME_LOWER = APP_NAME.lower()
    APP_DB_EXT = ".kdbx"

    # File: view/main_window.py
    BTN_ADD_ENTRY = "Add Entry"
    CTX_MENU_COPY = "Copy OTP code"
    CTX_MENU_EXPORT = "Export entry"
    CTX_MENU_EDIT = "Edit entry"
    CTX_MENU_DELETE = "Delete entry"

    WARN_DUPLICATE_ENTRY = "Duplicate entry"
    WARN_DUPLICATE_ENTRY_BODY = "This entry already exists in your database"

    NOTIF_COPY_SUCCESS = "OTP code copied to clipboard"

    TITLE_DELETE_ENTRY = "Delete entry"
    BODY_DELETE_ENTRY = "Are you sure you want to delete this entry?"

    # File: view/widget_add_entry.py
    TITLE_ADD_ENTRY = "Add Entry"

    BTN_CANCEL = "Cancel"
    BTN_LOAD_IMAGE = "Load Image"
    BTN_PASTE_IMAGE = "Paste Image"
    BTN_READ_QR_CODE = "Read QR Code"

    FILTER_FILE_IMAGE = "Image Files (*.png *.jpg *.bmp)"
    IMAGE_PNG = "PNG"

    WARN_INVALID_QR = "Invalid QR Code"
    WARN_INVALID_QR_BODY = "This is not a valid QR code."

    WARN_INVALID_IMAGE_SIZE = "Invalid image size"
    WARN_INVALID_IMAGE_SIZE_BODY = "Image size is too large."

    # File: view/widget_edit_entry.py
    TITLE_EDIT_ENTRY = "Edit Entry"
    PHOLDER_NEW_USERNAME = "New username"
    BTN_SAVE_USERNAME = "Save"

    # File: view/create_db.py
    TITLE_CREATE_DB = "Create Database"
    LABEL_DB_NAME = "Database name"
    LABEL_DB_LOCATION = "Database location"
    PHOLDER_DB_LOCATION = "Select location"
    LABEL_DB_PASSWORD = "Database password"
    LABEL_DB_PASSWORD_CONFIRM = "Confirm password"

    BTN_DIALOG = "..."
    TITLE_DB_DIALOG = "Select a location for the database"
    BTN_CREATE_DB = "Create database"

    # File: view/widget_export_entry.py
    TITLE_EXPORT_ENTRY = "Export Entry"
    BTN_COPY_SECRET = "Copy secret"

    # File: view/load_file.py
    TITLE_CHOOSE_DB_LOCATION = "Choose Database Location"
    TITLE_LOAD_DB = "Load Database"
    TITLE_LOAD_IMAGE = "Load QR Code Image"
    FILTER_IMAGE = "Image files (*.png *.jpg *.bmp)"
    FILTER_DB = "KeePass database (*.kdbx)"

    # File: utils/config.py
    APP_CONFIG_NAME = APP_NAME_LOWER + ".ini"
    APP_CONFIG_PATH = get_config_path(APP_NAME_LOWER, APP_CONFIG_NAME)
    DB_PATH_KEY = "database_path"

    # Etc
    UTF_8 = "utf-8"
