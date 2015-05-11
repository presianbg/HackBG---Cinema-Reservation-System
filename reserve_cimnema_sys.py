from magic_reservation_system import CinemaReservation
from settings import DB_NAME
import sqlite3
import copy

reserve_msg = [("Step 1(user)>", str),
               ("Step 2(number of tickets)>", int),
               ("Step 3(choose a movie)>", int),
               ("Step 4(choose projection)>", int),
               ("Step 5(choose seats for ", tuple),
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
            recv_data = {}
            current_reservation = copy.deepcopy(reserve_msg)

            while current_reservation:

                current_step, data_type = current_reservation[0]
                current_reservation.pop(0)

                if current_step == reserve_msg[2][0]:
                    cur_step_data = get_movie(current_step, data_type)

                elif current_step == reserve_msg[3][0]:
                    cur_step_data = get_projection(current_step, data_type, recv_data['Step-3'])

                elif current_step == reserve_msg[4][0]:
                    cur_step_data = check_seats(recv_data['Step-2'], current_step, data_type, recv_data['Step-4'])
                else:
                    cur_step_data = take_user_data(current_step, data_type)

                if not cur_step_data:
                    print ('Reservation process aborted!')
                    break

                step_key = len(reserve_msg) - len(current_reservation)
                recv_data['Step-{}'.format(step_key)] = cur_step_data

        elif CinemaReservation.is_command(command, "exit"):
            db_connection.close()
            break

        else:
            if command[0] is '':
                continue
            print(CinemaReservation.trigger_unknown_command())


def get_movie(step, data_type):
    print (CinemaReservation.show_movies(db_connection))
    movie_id = None
    while not CinemaReservation.show_movie_projections(db_connection, movie_id):
        movie_id = take_user_data(step, data_type)
        if not movie_id:
            return False
    return movie_id


def get_projection(step, data_type, movie_id):
    print (CinemaReservation.show_movie_projections(db_connection, movie_id))
    l_id = []
    proj_ids = CinemaReservation.get_id_of_projections(db_connection, movie_id)
    for ids in proj_ids:
        l_id.append(ids[0])

    proj_id = None
    while proj_id not in l_id:
        proj_id = take_user_data(step, data_type)
        if not proj_id:
            return False
    return proj_id


def reservation_flow(step):

    reserv_funcs = {"Step 3(choose a movie)>": "CinemaReservation.show_movies(db_connection)",
                    "Step 4(choose projection)>": "CinemaReservation.show_movie_projections(db_connection, cur_step_data)",
                    "Step 5(choose seats for ": "CinemaReservation.show_hall_layout(db_connection, cur_step_data)"
                    }
    if step in reserv_funcs:
        return reserv_funcs[step]


def check_seats(numb_of_seats, msg, d_type, proj_id):
    print (CinemaReservation.show_hall_layout(db_connection, proj_id))
    seats = []
    for tick_num, seat in enumerate(range(numb_of_seats)):
        while True:
            try:
                data = input(msg + 'Tiket-{}>'.format(tick_num + 1))
                if is_give_up(data):
                    return False
                seat_pos = d_type(int(x.strip()) for x in data.split(','))
                seats.append(seat_pos)
                break
            except Exception as e:
                print (e)
                continue

    return seats


def take_user_data(step, data_type):

    while True:
        try:
            data = input(step)
            if is_give_up(data):
                return False
            if not data:
                continue
            else:
                return data_type(data)
        except Exception as e:
            print(e)


def is_give_up(data):
    return data == 'give_up'

if __name__ == '__main__':
    main()
