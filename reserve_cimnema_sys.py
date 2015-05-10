from magic_reservation_system import CinemaReservation
from settings import DB_NAME
import sqlite3

reserve_msg = [("Step 1(user)>", str),
               ("Step 2(number of tickets)>", int),
               ("Step 3(choose a movie)>", int),
               ("Step 4(choose projection)>", int),
               ("Step 5(choose seats)>", int),
               ("Step 6(Confirm - type 'finalize')>", str)]

db_connection = sqlite3.connect(DB_NAME)


def main():

    while True:
        command = CinemaReservation.parse_command(input("Enter command>"))

        if CinemaReservation.is_command(command, "help"):
            print(CinemaReservation.create_help())

        elif CinemaReservation.is_command(command, "show_movies"):
            print (CinemaReservation.show_movies(db_connection))

        elif CinemaReservation.is_command(command, "show_projections"):
            if len(command) == 3:
                print(CinemaReservation.show_movie_projections(db_connection, command[1], command[2]))
            elif len(command) == 2:
                print(CinemaReservation.show_movie_projections(db_connection, command[1]))
            else:
                print("No Movie Selected")

        elif CinemaReservation.is_command(command, "make_reservation"):
            print ('You are about to make reservation! Just folloow the steps. You can give_up @ any time :)')
            rsv_data = {}

            for num, msg in enumerate(reserve_msg):

                if reservation_flow(msg):
                    if not eval(reservation_flow(msg)):
                        while not eval(reservation_flow(msg)):
                            print ('Invalid Choice')
                            input_data = msg[1](input(reserve_msg[num-1][0]))
                    print (eval(reservation_flow(msg[0])))

                if num == 4:
                    check_seats(rsv_data['Step-2'])
                else:
                    input_data = msg[1](input(msg[0]))

                if input_data == "give_up":
                    print ('You Canceled your reservation!')
                    break

                rsv_data['Step-{}'.format(num+1)] = input_data

        elif CinemaReservation.is_command(command, "exit"):
            db_connection.close()
            break

        else:
            if command[0] is '':
                continue
            print(CinemaReservation.trigger_unknown_command())


def reservation_flow(step):

    reserv_funcs = {"Step 3(choose a movie)>": "CinemaReservation.show_movies(db_connection)",
                    "Step 4(choose projection)>": "CinemaReservation.show_movie_projections(db_connection, input_data)",
                    "Step 5(choose seats)>": "CinemaReservation.show_hall_layout(db_connection, input_data)"
                    }
    if step in reserv_funcs:
        return reserv_funcs[step]


def check_seats(numb_of_seats):
    print ('CHecking {} seats'.format(numb_of_seats))
    seat_pos = input(reserve_msg[4])
    print (seat_pos)

if __name__ == '__main__':
    main()
