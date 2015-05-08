from magic_reservation_system import CinemaReservation
from settings import DB_NAME
import sqlite3


def main():

    db_connection = sqlite3.connect(DB_NAME)

    while True:
        command = CinemaReservation.parse_command(input("Enter command>"))

        if CinemaReservation.is_command(command, "help"):
            print(CinemaReservation.create_help())

        elif CinemaReservation.is_command(command, "show_movies"):
            print (CinemaReservation.show_movies(db_connection))

        elif CinemaReservation.is_command(command, "show_movie_projections"):
            if len(command) > 2:
                print(CinemaReservation.show_movie_projections(db_connection, command[1], command[2]))
            else:
                print(CinemaReservation.show_movie_projections(db_connection, command[1]))

        elif CinemaReservation.is_command(command, "exit"):
            db_connection.close()
            break


if __name__ == '__main__':
    main()
