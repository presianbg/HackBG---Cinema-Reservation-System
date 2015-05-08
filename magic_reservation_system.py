import readline
import sqlite3
from tabulate import tabulate


class CinemaReservation:

    GET_MOVIES_BY_RATING = '''
        SELECT * FROM Movies ORDER BY rating DESC
    '''

    GET_PROJECTIONS = '''
        SELECT * FROM Projections
        WHERE movie_id = ? AND projection_date LIKE ?
    '''

    GET_MOVIE_NAME_BY_ID = '''
        SELECT name FROM Movies
        WHERE id = ?
    '''

    @staticmethod
    def create_help():
        help = ["Here is the list of commands:",
                "",
                "show_movies                             : Prints all movies ORDERed BY rating",
                "show_projections <movie_id> [<date>]>   : Prints all projections of a given movie for the given date (date is optional).",
                "make_reservation                        : Starts the reservation proccess",
                "cancel_reservation <name>               : Disintegrate given person's reservation",
                "exit                                    : Exits reservation system"]
        return "\n".join(help)

    @staticmethod
    def parse_command(command):
        return tuple(command.split(" "))

    @staticmethod
    def is_command(command_tuple, command_string):
        return command_tuple[0] == command_string

    @staticmethod
    def trigger_unknown_command():
        unknown_command = ["Error: Unknown command!",
                           "Why don't you type help,",
                           "to see a list of commands."]

        return "\n".join(unknown_command)

    @classmethod
    def show_movies(cls, connection):
        cursor = connection.cursor()
        cursor.execute(cls.GET_MOVIES_BY_RATING)
        movies_by_rating = cursor.fetchall()
        headers = ["id", "Movie Name", "Movie Rating"]
        table_cols = [0, 1, 2]
        return cls.make_tabulate_tabl(headers, table_cols, movies_by_rating)

    @classmethod
    def show_movie_projections(cls, connection, movie_id, date='%%'):
        cursor = connection.cursor()

        cursor.execute(cls.GET_PROJECTIONS, (movie_id, date))
        projections_by_movie = cursor.fetchall()

        cursor.execute(cls.GET_MOVIE_NAME_BY_ID, (movie_id,))
        movie_name = cursor.fetchone()

        if not projections_by_movie:
            return 'There are No Movies on that DATE'

        headers = ["id", "date", "time", "type"]
        table_cols = [0, 3, 4, 2]
        print (movie_name[0])
        return cls.make_tabulate_tabl(headers, table_cols, projections_by_movie)

    @classmethod
    def make_tabulate_tabl(cls, headers, table_cols, table_data):
        pptable = []
        for row in table_data:
            pptable.append([row[i] for i in table_cols])
        return tabulate(pptable, headers, tablefmt="fancy_grid")
