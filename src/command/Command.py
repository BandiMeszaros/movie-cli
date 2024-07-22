from src.utils.db_conn import movie_db
class Command:

    def __init__(self):
        self.database = movie_db

    def __call__(self):
        self.run()

    def run(self):
        pass

