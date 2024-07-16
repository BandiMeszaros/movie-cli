import sqlite3


class DbConn:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()
