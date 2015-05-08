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

    GET_AVAIL_SEATS_FOR_PROJECTION = """
    SELECT COUNT(id) AS available_seats FROM Reservations 
    """

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
        headers = ["id", "Movie Name", "Movie Rating"]
        cursor = connection.cursor()
        cursor.execute(cls.GET_MOVIES_BY_RATING)
        movies_by_rating = cursor.fetchall()
        for row in movies_by_rating:
            pptable.append([row[0], row[1], row[2]])
        return tabulate(pptable, headers, tablefmt="fancy_grid")

    @classmethod
    def show_movie_projections(cls, connection, movie_id, date='%%'):
        cursor = connection.cursor()
        cursor.execute(cls.GET_PROJECTIONS, (movie_id, date))
        projections_by_movie = cursor.fetchall()
        if not projections_by_movie:
            return 'There are No Movies on that DATE'
        pptable = []
        headers = ["id", "date", "time", "type"]
        for row in projections_by_movie:
            # taken_seats = cursor.execute(cls.GET_AVAIL_SEATS_FOR_PROJECTION), (row[0],)
            pptable.append([row[0], row[3], row[4], row[2]])
        return tabulate(pptable, headers, tablefmt="fancy_grid")
