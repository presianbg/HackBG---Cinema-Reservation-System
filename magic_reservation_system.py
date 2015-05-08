import readline
import sqlite3
from tabulate import tabulate


class CinemaReservation:

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

    @classmethod
    def parse_command(cls, command):
        return tuple(command.split(" "))

    @classmethod
    def show_movies(cls, connection):
        pptable = []
        headers = ["Movie Name", "Movie Rating"]
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM Movies ORDER BY rating DESC''')
        movies_by_rating = cursor.fetchall()
        for row in movies_by_rating:
            pptable.append(row[1], row[2])
        return tabulate(pptable, headers, tablefmt="fancy_grid")

    @classmethod
    def is_command(cls, command_tuple, command_string):
        return command_tuple[0] == command_string
