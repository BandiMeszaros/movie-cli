from src.command.Command import Command
import re
from datetime import datetime
from src.utils.logger_setup import loggerCursor
class AddCommand(Command):

    def __init__(self, person=False, movie=False):
        super().__init__()
        self.person = person
        self.movie = movie

    def run(self):
        if self.person:
            self.add_person()
        if self.movie:
            self.add_movie()

    def add_person(self):
        name = input("Name: ")
        while True:
            birth_year = input("Year of birth: ")
            if birth_year.isdigit() and 1900 <= int(birth_year) <= datetime.now().year:
                break
            loggerCursor.error("Invalid year. Please enter a valid year between 1900 and current year.")
        query = f"INSERT INTO Person (name, birth_year) VALUES ('{name}', {birth_year})"
        loggerCursor.debug(f"{query}")
        self.database.cursor.execute(query)
        self.database.conn.commit()
        loggerCursor.info(f"Person '{name}' added successfully.")

    def add_movie(self):
        title = input("Title: ")

        while True:
            length = input("Length (hh:mm): ")
            if re.match(r'^\d{2}:\d{2}$', length):
                hours, minutes = map(int, length.split(':'))
                if 0 <= hours <= 23 and 0 <= minutes <= 59:
                    total_minutes = hours * 60 + minutes
                    break
            loggerCursor.error("Bad input format (hh:mm), try again!")

        while True:
            director_name = input("Director: ")
            director = self.database.cursor.execute(f"SELECT person_id, birth_year FROM Person WHERE name = '{director_name}'").fetchone()
            if director:
                director_id = director[0]
                break
            loggerCursor.error(f"We could not find \"{director_name}\", try again!")

        while True:
            release_year = input("Released in: ")
            if int(release_year) - int(director[1]) < 0:
                loggerCursor.error(f"Director is to young, to be in this movie, try again!")
                continue
            if release_year.isdigit() and 1900 <= int(release_year) <= datetime.now().year:
                break
            loggerCursor.error("Invalid year. Please enter a valid year between 1900 and current year.")

        movie_id = self.database.cursor.execute(f"INSERT INTO Movie (title, length_minutes, director_id, release_year) VALUES ('{title}', {total_minutes}, {director_id}, {release_year})")
        self.database.conn.commit()
        movie_id = movie_id.lastrowid

        loggerCursor.info("Starring (type 'exit' to finish):")
        while True:
            actor_name = input()
            if actor_name.lower() == 'exit':
                break
            actor = self.database.cursor.execute(f"SELECT person_id, birth_year FROM Person WHERE name = '{actor_name}'").fetchone()
            if actor:
                if int(release_year)-int(actor[1]) < 0:
                    loggerCursor.error(f"Actor is to young, to be in this movie, try again!")
                    continue
                loggerCursor.debug(f"INSERT INTO MovieActor (movie_id, actor_id) VALUES ({movie_id}, {actor[0]});")
                self.database.cursor.execute(f"INSERT INTO MovieActor (movie_id, actor_id) VALUES ({movie_id}, {actor[0]});")
                self.database.conn.commit()
            else:
                loggerCursor.info(f"We could not find \"{actor_name}\", try again!")

        print(f"Added movie {title} to the database with ID {movie_id}.")
