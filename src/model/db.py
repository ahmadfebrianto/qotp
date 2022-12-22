from urllib.parse import unquote

import pykeepass
from pyotp import parse_uri


class Database:
    instance = None
    db_path = None

    def create(self, db_path, db_password):
        self.instance = pykeepass.create_database(db_path, db_password)
        self.db_path = db_path

    def open(self, db_path, db_password):
        self.instance = pykeepass.PyKeePass(db_path, password=db_password)
        self.db_path = db_path


class Entry(Database):
    def __init__(self, uri):
        self.otp = parse_uri(unquote(uri))

    def save(self):
        title = self.otp.issuer
        username = self.otp.name
        password = self.otp.secret
        url = self.otp.provisioning_uri()

        self.instance.add_entry(
            self.instance.root_group, title, username, password, url=url
        )
        self.instance.save()

    def delete(self):
        pass


