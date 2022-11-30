from pathlib import Path

import pykeepass


class OTPAccount:
    def __init__(self, name, username, password, url, otp_secret):
        self.name = name
        self.username = username
        self.password = password
        self.url = url
        self.otp_secret = otp_secret

    def __str__(self):
        return f"{type(self).__name__}({self.name}, {self.username}, {self.url})"


class Database:
    def create_db(self, db_path, db_password):
        db = pykeepass.create_database(db_path, db_password)
        return db

    def open_db(self, db_path, db_password):
        db = pykeepass.PyKeePass(db_path, password=db_password)
        return db
