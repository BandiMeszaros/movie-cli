import re
import sqlite3
from src.utils.logger_setup import loggerCursor

class DbConn:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.create_function("REGEXP", 2, self.regexp)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def regexp(self, expr, item):
        return re.search(expr, item) is not None


try:
    movie_db = DbConn('movieDb')
    loggerCursor.info('Connected to database...')
except Exception as e:
    loggerCursor.error('Failed to connect to database: %s', e)
    exit(1)