import select_queries as sq
from database_api import CarSharingDataBase

BOLD = '\033[1m'
END = '\033[0m'


def view_help(db):
    print("Write " + BOLD + "c" + END + " if you want to see the list of cars, \n"
          + "write " + BOLD + "cp" + END + " if you want to see the list of car parts, \n"
          + "write " + BOLD + "ct" + END + " if you want to see the list of car types, \n"
          + "write " + BOLD + "charst" + END + " if you want to see the list of acts of charging, \n"
          + "write " + BOLD + "char" + END + " if you want to see the list of charing stations, \n"
          + "write " + BOLD + "cust" + END + " if you want to see the list of customers, \n"
          + "write " + BOLD + "loc" + END + " if you want to see the list of locations, \n"
          + "write " + BOLD + "charger" + END + " if you want to see the charging plugs, \n"
          + "write " + BOLD + "providing" + END + " is you want to see the list of USED car parts, \n"
          + "write " + BOLD + "provider" + END + " if you want to see the list of providers, \n"
          + "write " + BOLD + "rep" + END + " if you want to see the list of repair info, \n"
          + "write " + BOLD + "rides" + END + " if you want to see the list of rides, \n"
          + "write " + BOLD + "work" + END + " if you want to see the list of workshops, \n"
          + "write " + BOLD + "workparts" + END + " if you want to see the list of car parts present in workshop\n"
          + "write " + BOLD + "help" + END + " if you want to see this text \n"
          + "write " + BOLD + "q" + END + " if you want to quit")
    viewing(db)


def viewing(db):
    while True:
        ans = input()
        sql = ''
        if ans == 'c':
            sql = "SELECT * FROM car"
        elif ans == 'cp':
            sql = "SELECT * FROM car_part"
        elif ans == 'loc':
            sql = "SELECT * FROM location"
        elif ans == 'ct':
            sql = "SELECT * FROM car_type"
        elif ans == 'charst':
            sql = "SELECT * FROM charge"
        elif ans == 'char':
            sql = "SELECT * FROM charging_station"
        elif ans == 'cust':
            sql = "SELECT * FROM customer"
        elif ans == 'charger':
            sql = "SELECT * FROM plug"
        elif ans == 'providing':
            sql = "SELECT * FROM provide_car_parts"
        elif ans == 'provider':
            sql = "SELECT * FROM provider"
        elif ans == 'rep':
            sql = "SELECT * FROM repair"
        elif ans == 'rides':
            sql = "SELECT * FROM ride"
        elif ans == 'work':
            sql = "SELECT * FROM workshop"
        elif ans == 'workparts':
            sql = "SELECT * FROM workshop_car_part"
        elif ans == 'q':
            start(db)
        elif ans == 'help':
            view_help(db)
        else:
            print("No such table")

        if sql != '':
            db.execute_query(sql)
            results = db.get_answer()
            for row in results:
                print(row)


def queries(db):
    while True:
        ans = input(
            "Write the number " + BOLD + "(1 - 9)" + END + " of query which you want to check or all. \n "
            + "Press " + BOLD + "q" + END + " for exit\n")
        if ans == '1':
            print(sq.find_car(db, "Red", "AN", "Day7", "2018-11-20"))
        elif ans == '2':
            print(sq.number_sockets_occupied(db, 1, "2018-11-20"))
        elif ans == '3':
            print(sq.week_statistic(db))
        elif ans == '4':
            print(sq.twice_charge(db, "Day7"))
        elif ans == '5':
            print(sq.ride_statistic(db, '2018-11-20'))
        elif ans == '6':
            print(sq.popular_travel(db))
        elif ans == '7':
            sq.delete_car_ten_percentage(db)
            print("Done")
        elif ans == '8':
            print(sq.charge_amount(db, '2017-10-01'))
        elif ans == '9':
            print(sq.often_require_car_part(db))
        elif ans == '10':
            print(sq.car_with_expensive_service(db))
        elif ans == 'all':
            print(sq.find_car(db, "Red", "AN", "Day7", "2018-11-20"))
            print(sq.number_sockets_occupied(db, 1, "2018-11-20"))
            print(sq.week_statistic(db))
            print(sq.twice_charge(db, "Day7"))
            print(sq.ride_statistic(db, '2018-11-20'))
            print(sq.popular_travel(db))
            sq.delete_car_ten_percentage(db)
            print(sq.charge_amount(db, '2017-10-01'))
            print(sq.often_require_car_part(db))
            print(sq.car_with_expensive_service(db))
        elif ans == 'q':
            start(db)


def start(db):
    while True:
        print("DMD Project by Amir Subaev, Vyacheslav Vasilev, Natalia Tupikina")
        print("Write " + BOLD + "v" + END + " is you want to see some table, \n"
              + "write " + BOLD + "t" + END + " to check select quieries, \n"
              + "write " + BOLD + "q" + END + " to quit.")
        ans = input()
        if ans == 't':
            queries(db)
        elif ans == "v":
            view_help(db)
        elif ans == "q":
            db.close_db()
            exit()


if __name__ == '__main__':
    db = CarSharingDataBase()
    ans = input("Do you want to recreate the database with random data? May take a long time [y/N] ")
    if ans == 'y':
        sq.sample_start(db)
    start(db)
