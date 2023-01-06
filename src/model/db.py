from urllib.parse import unquote

import pykeepass
from pyotp import parse_uri

from utils.common import unpack_entry


class Database:
    _instance = None

    def create(self, db_path, db_password):
        self._instance = pykeepass.create_database(db_path, db_password)

    def open(self, db_path, db_password):
        self._instance = pykeepass.PyKeePass(db_path, password=db_password)

    def get_entry(self, title_username):
        title, username = unpack_entry(title_username)
        entry = self._instance.find_entries(title=title, username=username, first=True)
        return entry

    @property
    def entries(self):
        return self._instance.entries

    def add_entry(self, uri):
        uri = unquote(uri)
        otp = parse_uri(uri)

        self._instance.add_entry(
            self._instance.root_group,
            title=otp.issuer,
            username=otp.name,
            password=otp.secret,
            otp=uri,
        )
        self._instance.save()

    def update_entry(self, title_username, new_title, new_username):
        entry = self.get_entry(title_username)
        entry.title = new_title
        entry.username = new_username
        self._instance.save()

    def delete_entry(self, title_username):
        entry = self.get_entry(title_username)
        self._instance.delete_entry(entry)
        self._instance.save()

    def entry_exists(self, uri):
        uri = unquote(uri)
        entry = self._instance.find_entries(otp=uri, first=True)
        return entry is not None

    def get_otp_code(self, title_username):
        entry = self.get_entry(title_username)
        otp = parse_uri(entry.otp)
        return otp.now()

    def get_secret(self, title_username):
        entry = self.get_entry(title_username)
        return entry.password

    def get_uri(self, title_username):
        entry = self.get_entry(title_username)
        return entry.otp


db = Database()
