from src.command.Command import Command
import re
from datetime import datetime
from src.utils.logger_setup import loggerCursor
class DeleteCommand(Command):

    def __init__(self, person=False, name=None):
        super().__init__()
        self.person = person
        self.name = name
    def run(self):
        if self.person:
            self.delete_person()

    def delete_person(self):
        name = input("Name: ")
        while True:
            query = f"SELECT person_id, birth_year FROM Person WHERE name = '{name}'"
            person = self.database.cursor.execute(query).fetchone()
            if person:
                query = f"SELECT COUNT(*) FROM Movie WHERE director_id = {person[0]}"
                count = self.database.cursor.execute(query).fetchone()[0]
                if count == 0:
                    break
                else:
                    loggerCursor.error(f"Person '{name}' has directed {count} movies, try again!")
                    return
            loggerCursor.error(f"We could not find \"{name}\", try again!")
        query = f"DELETE FROM Person WHERE name = '{name}'"
        loggerCursor.debug(f"{query}")
        self.database.cursor.execute(query)
        self.database.conn.commit()
        query = f"DELETE FROM MovieActor WHERE actor_id = {person[0]}"
        self.database.cursor.execute(query)
        self.database.conn.commit()
        loggerCursor.info(f"Person '{name}' deleted successfully.")
