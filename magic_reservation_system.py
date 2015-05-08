import readline
import sqlite3
from tabulate import tabulate


class CinemaReservation:

    GET_MOMIVES_BY_RATING = '''
        SELECT * FROM Movies ORDER BY rating DESC
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

    @classmethod
    def show_movies(cls, connection):
        pptable = []
        headers = ["Movie Name", "Movie Rating"]
        cursor = connection.cursor()
        cursor.execute(cls.GET_MOMIVES_BY_RATING)
        movies_by_rating = cursor.fetchall()
        for row in movies_by_rating:
            pptable.append(row[1], row[2])
        return tabulate(pptable, headers, tablefmt="fancy_grid")

    @classmethod
    def show_movie_projections(cls, connection, movie_id, date='*'):
        pass
