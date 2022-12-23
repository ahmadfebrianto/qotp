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

    def add_entry(self, uri):
        uri = unquote(uri)
        otp = parse_uri(uri)

        self.instance.add_entry(
            self.instance.root_group,
            title=otp.issuer,
            username=otp.name,
            password=otp.secret,
            otp=uri,
        )
        self.instance.save()

db = Database()
