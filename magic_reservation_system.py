import readline
from tabulate import tabulate


class CinemaReservation:

    HALL_SEATS = 100
    HALL_ROWS = 10
    HALL_COLS = 10

    GET_MOVIES_BY_RATING = '''SELECT * FROM Movies
        ORDER BY rating DESC
    '''

    GET_PROJECTIONS = '''SELECT Projections.*,
        (SELECT name FROM Movies WHERE Movies.id = Projections.movie_id),
        ? - (SELECT COUNT(id) FROM Reservations WHERE Reservations.projection_id = Projections.id) AS free_seats FROM Projections
        WHERE movie_id = ? AND projection_date LIKE ?
        ORDER BY projection_date ASC
    '''

    GET_TAKEN_SEATS_FOR_PROJ = '''SELECT row, col FROM Reservations WHERE projection_id = ?'''

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

        cursor.execute(cls.GET_PROJECTIONS, (cls.HALL_SEATS, movie_id, date))
        projections_by_movie = cursor.fetchall()

        if not projections_by_movie:
            return 'There are No Movies on that DATE'

        headers = ["id", "date", "time", "type", "free_seats"]
        table_cols = [0, 3, 4, 2, 6]
        print (projections_by_movie[0][5])
        return cls.make_tabulate_tabl(headers, table_cols, projections_by_movie)

    @classmethod
    def show_hall_layout(cls, connection, projection_id):
        headers = ['R/C']
        headers += [i+1 for i in range(cls.HALL_COLS)]
        table_cols = [i for i in range(cls.HALL_COLS + 1)]
        data = []

        cursor = connection.cursor()
        cursor.execute(cls.GET_TAKEN_SEATS_FOR_PROJ, (projection_id, ))
        taken_seats = cursor.fetchall()

        for row in range(cls.HALL_ROWS):
            data.append([row + 1])
            for col in range(cls.HALL_COLS + 1):
                if (row+1, col+1) in taken_seats:
                    data[row].append('_X_')
                else:
                    data[row].append('FREE')
        return cls.make_tabulate_tabl(headers, table_cols, data)

    @classmethod
    def make_tabulate_tabl(cls, headers, table_cols, table_data):
        pptable = []
        for row in table_data:
            pptable.append([row[i] for i in table_cols])
        return tabulate(pptable, headers, tablefmt="fancy_grid")
