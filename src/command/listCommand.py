from src.command.Command import Command
from src.utils.logger_setup import loggerCursor

class ListCommand(Command):
    def __init__(self, verbose=False, title_regex=None, director_regex=None, actor_regex=None,
                 list_asc=False, list_desc=False):
        super().__init__()
        self.verbose = verbose
        self.title_regex = title_regex
        self.director_regex = director_regex
        self.actor_regex = actor_regex
        self.list_asc = list_asc
        self.list_desc = list_desc

    def run(self):
        if self.verbose:
            output = self.query_movies_verbose()
            for movie, actors in output:
                print(self.base_line_output(movie[1], movie[2], movie[3], movie[4]))
                print('Starring:')
                for actor in actors:
                    age = movie[3] - actor[1]
                    print(f"\t{actor[0]} at age: {age}")

        else:
            output = self.query_movies()
            for movie in output:
                print(self.base_line_output(movie[1], movie[2], movie[3], movie[4]))

    @staticmethod
    def base_line_output(title, director, year, length):
        return f"{title} by {director} in {year}, {length}"

    def query_movies(self):
        query = """
               SELECT DISTINCT m.movie_id, m.title, p.name as director, m.release_year, m.length_minutes
               FROM Movie m
               JOIN Person p ON m.director_id = p.person_id
               LEFT JOIN MovieActor ma ON m.movie_id = ma.movie_id
               LEFT JOIN Person a ON ma.actor_id = a.person_id
               """

        conditions = []

        if self.title_regex:
            conditions.append(f"m.title REGEXP {self.title_regex}")
        if self.director_regex:
            conditions.append(f"p.name REGEXP {self.director_regex}")
        if self.actor_regex:
            conditions.append(f"a.name REGEXP {self.actor_regex}")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        if self.list_asc:
            query += " ORDER BY m.length_minutes ASC, m.title ASC"
        elif self.list_asc:
            query += " ORDER BY m.length_minutes DESC, m.title ASC"
        else:
            query += " ORDER BY m.title ASC"

        loggerCursor.debug(query)
        query_output = self.database.cursor.execute(query)
        movies = query_output.fetchall()

        return movies

    def query_movies_verbose(self):
        movies = self.query_movies()
        for movie in movies:
            actor_query = f"""
                       SELECT p.name, p.birth_year
                       FROM MovieActor ma
                       JOIN Person p ON ma.actor_id = p.person_id
                       WHERE ma.movie_id = {movie[0]}
                       """

            actor_cursor = self.database.cursor.execute(actor_query)
            actors = actor_cursor.fetchall()
            yield movie, actors
