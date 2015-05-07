import readline
import sqlite3


class CinemaReservation:

    def __init__(self, database_name):
        self.db_conn = sqlite3.connect(database_name)

    def create_help(self):
        help = ["Here is the list of commands:",
                "",
                "show_movies>                               : Prints all movies ORDERed BY rating",
                "show_projections <movie_id> [<date>]>      : Prints all projections of a given movie for the given date (date is optional).",
                "make_reservation                           : Starts the reservation proccess",
                "cancel_reservation <name>                  : Disintegrate given person's reservation",
                "exit                                       : Exits reservation system"]
        return "\n".join(help)

    def show_moves(self):
