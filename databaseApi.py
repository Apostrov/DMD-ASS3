import sqlite3
import random
import string
import datetime


def generate_random_int(length):
    return ''.join(random.choices(string.digits, k=length))


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_time():
    hour = ''.join((random.choice('012'))) + ''.join((random.choice('0123')))
    minute = ''.join(random.choices('012345', k=2))
    second = ''.join(random.choices('012345', k=2))

    return hour + ":" + minute + ":" + second


def generate_random_date():
    year = "2018"
    month = ''.join(random.choice('01')) + ''.join(random.choice('12'))
    day = ''.join(random.choice('012')) + generate_random_int(1)

    return year + "-" + month + "-" + day


class CarSharingDataBase:
    conn = sqlite3.connect('Car_sharing_service.db')
    cursor = conn.cursor()

    def open_db(self):
        self.conn = sqlite3.connect('Car_sharing_service.db')
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.conn.commit()
        self.conn.close()

    def execute_query(self, query, vals=''):
        self.cursor.execute(query, vals)
        self.conn.commit()

    def __init__(self):
        self.open_db()
        create_sql_file = open('create-table.sql', 'r').read()
        self.cursor.executescript(create_sql_file)
        self.conn.commit()

    # !!! Not secured from sql injection
    def select_table_column(self, table, column='*'):
        self.cursor.execute('select %s from %s' % (column, table))
        return self.cursor.fetchall()

    # Location
    def add_location(self, GPS, city, street, zip_code):
        vals = (GPS, city, street, zip_code)
        self.execute_query("insert into location values (?, ?, ?, ?)", vals)

    def add_random_location(self):
        GPS = generate_random_string(50)
        city = generate_random_string(50)
        street = generate_random_string(50)
        zip_code = generate_random_int(10)
        self.add_location(GPS, city, street, zip_code)

    # Charging station
    def add_charging_station(self, UID, available_sockets, price, time_of_charging, GPS):
        vals = (UID, available_sockets, price, time_of_charging, GPS)
        self.execute_query("insert into charging_station values (?, ?, ?, ?, ?)", vals)

    def add_random_charging_station(self):
        all_gps = self.select_table_column("location", "GPS")
        if len(all_gps) < 1:
            return

        UID = generate_random_int(10)
        available_sockets = generate_random_int(2)
        price = generate_random_string(3)
        time_of_charging = generate_random_int(2)
        GPS = random.choice(all_gps)[0]
        self.add_charging_station(UID, available_sockets, price, time_of_charging, GPS)

    # Plug
    def add_plug(self, UID, shape, size):
        vals = (UID, shape, size)
        self.execute_query("insert into plug values (?, ?, ?)", vals)

    def add_random_plug(self):
        all_uid = self.select_table_column("charging_station", "UID")
        if len(all_uid) < 1:
            return

        shape = generate_random_string(20)
        size = generate_random_int(2)
        UID = random.choice(all_uid)[0]

        self.add_plug(UID, shape, size)

    # Customer
    def add_customer(self, username, fullname, phone_number, email, GPS):
        vals = (username, fullname, phone_number, email, GPS)
        self.execute_query("insert into customer values (?, ?, ?, ?, ?)", vals)

    def add_random_customer(self):
        all_gps = self.select_table_column("location", "GPS")
        if len(all_gps) < 1:
            return

        username = generate_random_string(50)
        fullname = generate_random_string(50)
        phone_number = generate_random_string(20)
        email = generate_random_string(60)
        GPS = random.choice(all_gps)[0]

        self.add_customer(username, fullname, phone_number, email, GPS)

    # Workshop
    def add_workshop(self, WID, open_time, close_time, GPS):
        vals = (WID, open_time, close_time, GPS)
        self.execute_query("insert into workshop values (?, ?, ?, ?)", vals)

    def add_random_workshop(self):
        all_gps = self.select_table_column("location", "GPS")
        if len(all_gps) < 1:
            return

        WID = generate_random_int(10)
        open_time = generate_random_time()
        close_time = generate_random_time()
        GPS = random.choice(all_gps)[0]

        self.add_workshop(WID, open_time, close_time, GPS)

    # Car part
    def add_car_part(self, part_type, car_part, amount, specifications, WID):
        vals = (part_type, car_part, amount, specifications, WID)
        self.execute_query("insert into car_part values (?, ?, ?, ?, ?)", vals)

    def add_random_car_part(self):
        all_wid = self.select_table_column("workshop", "WID")
        if len(all_wid) < 1:
            return

        part_type = generate_random_string(40)
        car_type = generate_random_string(40)
        amount = generate_random_int(4)
        specifications = generate_random_string(100)
        WID = random.choice(all_wid)[0]

        self.add_car_part(part_type, car_type, amount, specifications, WID)

    # Provider
    def add_provider(self, phone_number, PID, GPS):
        vals = (phone_number, PID, GPS)
        self.execute_query("insert into provider values (?, ?, ?)", vals)

    def add_random_provider(self):
        all_gps = self.select_table_column("location", "GPS")
        if len(all_gps) < 1:
            return

        phone_number = generate_random_string(20)
        PID = generate_random_int(10)
        GPS = random.choice(all_gps)[0]

        self.add_provider(phone_number, PID, GPS)

    # Provide car parts
    def add_provide_car_parts(self, part_type, car_part, amount, specifications, PID, WID):
        vals = (part_type, car_part, amount, specifications, PID, WID)
        self.execute_query("insert into provide_car_parts values (?, ?, ?, ?, ?, ?)", vals)

    def add_random_provide_car_parts(self):
        all_wid = self.select_table_column("workshop", "WID")
        if len(all_wid) < 1:
            return

        all_pid = self.select_table_column("provider", "PID")
        if len(all_pid) < 1:
            return

        part_type = generate_random_string(40)
        car_type = generate_random_string(40)
        amount = generate_random_int(4)
        specifications = generate_random_string(100)
        PID = random.choice(all_pid)[0]
        WID = random.choice(all_wid)[0]

        self.add_provide_car_parts(part_type, car_type, amount, specifications, PID, WID)

    # Car
    def add_car(self, plate, type, broken, charge_amount, GPS, color):
        vals = (plate, type, broken, charge_amount, GPS, color)
        self.execute_query("insert into car values (?, ?, ?, ?, ?, ?)", vals)

    def add_random_car(self):
        plate = generate_random_string(10)
        type = generate_random_string(50)
        broken = False
        charge_amount = generate_random_int(2)
        GPS = generate_random_string(50)
        color = generate_random_string(10)

        self.add_car(plate, type, broken, charge_amount, GPS, color)

    # Ride
    def add_ride(self, plate, username, coordinate_a, coordinate_b, using_start, using_end):
        vals = (plate, username, coordinate_a, coordinate_b, using_start, using_end)
        self.execute_query("insert into ride values (?, ?, ?, ?, ?, ?)", vals)

    def add_random_ride(self):
        all_plate = self.select_table_column("car", "plate")
        if len(all_plate) < 1:
            return

        all_username = self.select_table_column("customer", "username")
        if len(all_username) < 1:
            return

        coordinate_a = generate_random_string(50)
        coordinate_b = generate_random_string(50)
        plate = random.choice(all_plate)[0]
        username = random.choice(all_username)[0]
        date = generate_random_date()
        using_start = date + " 00:00:00"
        using_end = date + generate_random_time()

        self.add_ride(plate, username, coordinate_a, coordinate_b, using_start, using_end)

    # Charge
    def add_charge(self, plate, UID, charged_datetime):
        vals = (plate, UID, charged_datetime)
        self.execute_query("insert into charge values (?, ?, ?)", vals)

    def add_random_charge(self):
        all_plate = self.select_table_column("car", "plate")
        if len(all_plate) < 1:
            return

        all_uid = self.select_table_column("charging_station", "UID")
        if len(all_uid) < 1:
            return

        plate = random.choice(all_plate)[0]
        UID = random.choice(all_uid)[0]
        charged_datetime = generate_random_date() + " " + generate_random_time()

        self.add_charge(plate, UID, charged_datetime)

    # Repair
    def add_repair(self, plate, WID):
        vals = (plate, WID)
        self.execute_query("insert into repair values (?, ?)", vals)

    def add_random_repair(self):
        all_plate = self.select_table_column("car", "plate")
        if len(all_plate) < 1:
            return

        all_wid = self.select_table_column("workshop", "WID")
        if len(all_wid) < 1:
            return

        plate = random.choice(all_plate)[0]
        WID = random.choice(all_wid)[0]

        self.add_repair(plate, WID)

    # Select Queries
    # First Query
    def find_car(self, color, plate, username, day):
        vals = (color, plate + "%", username, day)
        self.execute_query('''
        select car.plate from car
        join ride on car.plate = ride.plate
        where color = ? and car.plate like ? and username = ? and using_start >= ?
        ''', vals)
        plates = [x[0] for x in self.cursor.fetchall()]
        return plates

    # Second Query
    def number_sockets_occupied(self, uid, date):
        vals = (uid, date)
        self.execute_query('''
        select strftime('%H', charged_datetime) from charge
        join charging_station on charge.UID == charging_station.UID
        where charge.UID = ? and date(charged_datetime) = ?
        ''', vals)
        hours = [int(x[0]) for x in self.cursor.fetchall()]
        occupied = []
        for hour in range(24):
            occupied.append(hours.count(hour))

        return occupied

    # Third Query
    def week_statistic(self):
        self.execute_query('''
        select strftime('%H', using_start), strftime('%H', using_end) from ride
        where using_start BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime');
        ''')
        car_times = [[int(y) for y in x] for x in self.cursor.fetchall()]
        cars_duringtime = [0, 0, 0]  # morning (7AM - 10 AM), afternoon (12AM - 2PM) and evening (5PM - 7PM)
        for time in car_times:
            if (7 <= time[0] <= 10) or (7 <= time[1] <= 10):
                cars_duringtime[0] += 1
            if (12 <= time[0] <= 14) or (12 <= time[1] <= 14):
                cars_duringtime[1] += 1
            if (17 <= time[0] <= 19) or (17 <= time[1] <= 19):
                cars_duringtime[2] += 1
        cars_amount = len(self.select_table_column('car', 'plate'))
        cars_duringtime = [int(x / cars_amount * 100) for x in cars_duringtime]
        return cars_duringtime

    # Fourth Query
    def fourt(self):
        pass

    # Fifth Query
    def ride_statistic(self, day):
        vals = (day,)
        self.execute_query('''
        select using_start, using_end, coordinate_a, coordinate_b from ride
        where date(using_start) = ?
        ''', vals)
        times_and_coordinates = self.cursor.fetchall()
        durations = []
        for tandc in times_and_coordinates:
            time_start = datetime.datetime.strptime(tandc[0], '%Y-%m-%d %H:%M:%S')
            time_end = datetime.datetime.strptime(tandc[1], '%Y-%m-%d %H:%M:%S')
            durations.append(time_end - time_start)

        average_time = sum([x.seconds for x in durations]) / len(durations)
        return average_time

    # Another func
    # May take a long time
    def add_random_data(self, amount):
        for i in range(amount):
            self.add_random_location()
            self.add_random_charging_station()
            self.add_random_plug()
            self.add_random_customer()
            self.add_random_workshop()
            self.add_random_car_part()
            self.add_random_provider()
            self.add_random_provide_car_parts()
            self.add_random_car()
            self.add_random_ride()
            self.add_random_charge()
            self.add_random_repair()


if __name__ == '__main__':
    db = CarSharingDataBase()
    '''
    # Random test
    db.add_random_data(4)
    
    # Hand add
    db.add_location("gps", "ksz", "strt", 111)
    db.add_charging_station(12, 5, "10$", 10, "gps")
    db.add_plug(12, "shp", 10)
    db.add_customer("Day7", "7", "77", "777", "7777")
    db.add_workshop(21, "06:00:00", "20:00:00", "gps")
    db.add_car_part("part", "type", 120, "spec", 21)
    db.add_provider("phone_numb", 11, "gps")
    db.add_provide_car_parts("part", "type", 120, "spec", 11, 21)
    db.add_car("AN123", "B", False, 100, "gps1", "Red")
    db.add_ride("AN123", "Day7", "gps1", "gps", "2018-11-20 06:00:00", "2018-11-20 08:30:00")
    db.add_charge("AN123", 12, "2018-11-20 09:00:00")
    db.add_repair("AN123", 21)
    '''
    # Query
    print(db.find_car("Red", "AN", "Day7", "2018-11-20"))
    print(db.number_sockets_occupied(12, "2018-11-20"))
    print(db.week_statistic())
    print(db.ride_statistic('2018-11-20'))
    db.close_db()
