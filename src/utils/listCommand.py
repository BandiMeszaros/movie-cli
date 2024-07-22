class ListCommand:
    def __init__(self, verbose=False, title_regex=None, director_regex=None, actor_regex=None,
                 list_asc=False, list_desc=False):
        self.verbose = verbose
        self.title_regex = title_regex
        self.director_regex = director_regex
        self.actor_regex = actor_regex
        self.list_asc = list_asc
        self.list_desc = list_desc

    def base_line_output(self, title, director, year, length):
        return f"{title} by {director} in {year}, {length}"

    def query_movies(self):
        query = """
               SELECT DISTINCT m.id, m.title, p.name as director, m.release_year, m.length
               FROM movies m
               JOIN people p ON m.director_id = p.id
               LEFT JOIN movie_actors ma ON m.id = ma.movie_id
               LEFT JOIN people a ON ma.actor_id = a.id
               """

        conditions = []
        params = []

        if self.title_regex:
            conditions.append("m.title REGEXP %s")
            params.append(self.title_regex)
        if self.director_regex:
            conditions.append("p.name REGEXP %s")
            params.append(self.director_regex)
        if self.actor_regex:
            conditions.append("a.name REGEXP %s")
            params.append(self.actor_regex)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        if self.list_asc:
            query += " ORDER BY m.length ASC, m.title ASC"
        elif self.list_asc:
            query += " ORDER BY m.length DESC, m.title ASC"
        else:
            query += " ORDER BY m.title ASC"

        cursor = self.execute_query(query, tuple(params))
        movies = cursor.fetchall()

        if self.verbose:
            for movie in movies:
                actor_query = """
                       SELECT p.name, p.birth_year
                       FROM movie_actors ma
                       JOIN people p ON ma.actor_id = p.id
                       WHERE ma.movie_id = %s
                       """
                actor_cursor = self.execute_query(actor_query, (movie[0],))
                actors = actor_cursor.fetchall()
                yield (movie, actors)
        else:
            for movie in movies:
                yield movie
