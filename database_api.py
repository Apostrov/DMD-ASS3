import sqlite3
import random
import string


# Helpful functions
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
    year = "2017"
    month = ''.join(random.choice('01')) + ''.join(random.choice('12'))
    day = ''.join(random.choice('012')) + generate_random_int(1)
    if day == '00':
        day = '01'
    if month == '00':
        month = '01'
    return year + "-" + month + "-" + day


def generate_random_gps():
    latitude = random.uniform(40, 60)
    longitude = random.uniform(30, 130)
    return str(latitude) + ", " + str(longitude)


class CarSharingDataBase:
    conn = sqlite3.connect('Car_sharing_service.db')
    cursor = conn.cursor()

    def open_db(self):
        self.conn = sqlite3.connect('Car_sharing_service.db')
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.conn.commit()
        self.conn.close()

    def get_answer(self):
        return self.cursor.fetchall()

    def execute_query(self, query, vals=()):
        self.cursor.execute(query, vals)
        self.conn.commit()

    def __init__(self):
        self.open_db()
        create_sql_file = open('create-table.sql', 'r').read()
        self.cursor.executescript(create_sql_file)
        self.conn.commit()

    def recreate_all_tables(self):
        self.cursor.executescript('''
        drop table charge;
        drop table plug;
        drop table charging_station;
        drop table provide_car_parts;
        drop table provider;
        drop table repair;
        drop table ride;
        drop table car;
        drop table customer;
        drop table workshop_car_part;
        drop table car_part;
        drop table car_type;
        drop table workshop;
        drop table location;
        ''')
        self.conn.commit()
        self.__init__()

    # !!! Not secured from sql injection
    def select_table_column(self, table, column='*'):
        self.cursor.execute('select %s from %s' % (column, table))
        return self.cursor.fetchall()

    # !!! Not secured from sql injection
    def delete_by_condition(self, table, delete_condition):
        self.execute_query('delete from %s where %s' % (table, delete_condition))

    # Location
    def add_location(self, GPS, city, street, zip_code):
        vals = (GPS, city, street, zip_code)
        self.execute_query("insert into location values (?, ?, ?, ?)", vals)

    def add_random_location(self):
        GPS = generate_random_gps()
        city = generate_random_string(50)
        street = generate_random_string(50)
        zip_code = generate_random_int(10)
        self.add_location(GPS, city, street, zip_code)

    # Charging station
    def add_charging_station(self, available_sockets, price, time_of_charging, GPS):
        vals = (available_sockets, price, time_of_charging, GPS)
        self.execute_query(
            "insert into charging_station (available_sockets, price, time_of_charging, GPS) values (?, ?, ?, ?)", vals)

    def add_random_charging_station(self):
        all_gps = self.select_table_column("location", "GPS")
        if len(all_gps) < 1:
            return

        available_sockets = generate_random_int(2)
        price = generate_random_int(1)
        time_of_charging = generate_random_int(2)
        GPS = random.choice(all_gps)[0]
        self.add_charging_station(available_sockets, price, time_of_charging, GPS)

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

    # Car part
    def add_car_part(self, part_type, car_type, specifications):
        vals = (part_type, car_type, specifications)
        self.execute_query("insert into car_part (part_type, car_type, specifications) values (?, ?, ?)", vals)

    def add_random_car_part(self):
        all_car_type = self.select_table_column("car_type", "car_type")
        if len(all_car_type) < 1:
            return

        part_type = generate_random_string(40)
        car_type = random.choice(all_car_type)[0]
        specifications = generate_random_string(100)

        self.add_car_part(part_type, car_type, specifications)

    # Workshop
    def add_workshop(self, open_time, close_time, GPS):
        vals = (open_time, close_time, GPS)
        self.execute_query("insert into workshop (open_time, close_time, GPS) values (?, ?, ?)", vals)

    def add_random_workshop(self):
        all_gps = self.select_table_column("location", "GPS")
        if len(all_gps) < 1:
            return

        open_time = generate_random_time()
        close_time = generate_random_time()
        GPS = random.choice(all_gps)[0]

        self.add_workshop(open_time, close_time, GPS)

    # Workshop Car part
    def add_workshop_car_part(self, amount, part_ID, WID):
        vals = (amount, part_ID, WID)
        self.execute_query("insert into workshop_car_part values (?, ?, ?)", vals)

    def add_random_workshop_car_part(self):
        all_part_ID = self.select_table_column("car_part", "part_ID")
        if len(all_part_ID) < 1:
            return

        all_wid = self.select_table_column("workshop", "WID")
        if len(all_wid) < 1:
            return

        amount = generate_random_int(4)
        part_ID = random.choice(all_part_ID)[0]
        WID = random.choice(all_wid)[0]

        self.add_workshop_car_part(amount, part_ID, WID)

    # Provider
    def add_provider(self, phone_number, GPS):
        vals = (phone_number, GPS)
        self.execute_query("insert into provider (phone_number, GPS) values (?, ?)", vals)

    def add_random_provider(self):
        all_gps = self.select_table_column("location", "GPS")
        if len(all_gps) < 1:
            return

        phone_number = generate_random_string(20)
        GPS = random.choice(all_gps)[0]

        self.add_provider(phone_number, GPS)

    # Provide car parts
    def add_provide_car_parts(self, amount, part_ID, PID, WID, provided_date):
        vals = (amount, part_ID, PID, WID, provided_date)
        self.execute_query("insert into provide_car_parts values (?, ?, ?, ?, ?)", vals)

    def add_random_provide_car_parts(self):
        all_part_ID = self.select_table_column("car_part", "part_ID")
        if len(all_part_ID) < 1:
            return

        all_wid = self.select_table_column("workshop", "WID")
        if len(all_wid) < 1:
            return

        all_pid = self.select_table_column("provider", "PID")
        if len(all_pid) < 1:
            return

        amount = generate_random_int(4)
        part_ID = random.choice(all_part_ID)[0]
        PID = random.choice(all_pid)[0]
        WID = random.choice(all_wid)[0]
        provided_date = generate_random_date()

        self.add_provide_car_parts(amount, part_ID, PID, WID, provided_date)

    # Car type
    def add_car_type(self, car_type):
        vals = (car_type,)
        self.execute_query("insert into car_type values (?)", vals)

    def add_random_car_type(self):
        car_type = generate_random_string(20)

        self.add_car_type(car_type)

    # Car
    def add_car(self, plate, car_type, broken, charge_amount, GPS, color, purchase_date):
        vals = (plate, car_type, broken, charge_amount, GPS, color, purchase_date)
        self.execute_query("insert into car values (?, ?, ?, ?, ?, ?, ?)", vals)

    def add_random_car(self):
        all_car_type = self.select_table_column("car_type", "car_type")
        if len(all_car_type) < 1:
            return

        plate = generate_random_string(10)
        car_type = random.choice(all_car_type)[0]
        broken = False
        charge_amount = generate_random_int(2)
        GPS = generate_random_gps()
        color = generate_random_string(10)
        purchase_date = '2017-01-01'

        self.add_car(plate, car_type, broken, charge_amount, GPS, color, purchase_date)

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

        coordinate_a = generate_random_gps()
        coordinate_b = generate_random_gps()
        plate = random.choice(all_plate)[0]
        username = random.choice(all_username)[0]
        date = generate_random_date()
        using_end = date + " " + generate_random_time()
        using_start = using_end[:-6] + ":00:00"

        self.add_ride(plate, username, coordinate_a, coordinate_b, using_start, using_end)

    # Charge
    def add_charge(self, plate, UID, cost, charged_datetime):
        vals = (plate, UID, cost, charged_datetime)
        self.execute_query("insert into charge values (?, ?, ?, ?)", vals)

    def add_random_charge(self):
        all_plate = self.select_table_column("car", "plate")
        if len(all_plate) < 1:
            return

        all_uid = self.select_table_column("charging_station", "UID")
        if len(all_uid) < 1:
            return

        plate = random.choice(all_plate)[0]
        UID = random.choice(all_uid)[0]
        cost = generate_random_int(1)
        charged_datetime = generate_random_date() + " " + generate_random_time()

        self.add_charge(plate, UID, cost, charged_datetime)

    # Repair
    def add_repair(self, plate, WID, cost, repair_date):
        vals = (plate, WID, cost, repair_date)
        self.execute_query("insert into repair values (?, ?, ?, ?)", vals)

    def add_random_repair(self):
        all_plate = self.select_table_column("car", "plate")
        if len(all_plate) < 1:
            return

        all_wid = self.select_table_column("workshop", "WID")
        if len(all_wid) < 1:
            return

        plate = random.choice(all_plate)[0]
        WID = random.choice(all_wid)[0]
        cost = generate_random_int(2)
        repair_date = generate_random_date()

        self.add_repair(plate, WID, cost, repair_date)

    # May take a long time
    def add_random_data(self, amount):
        print("Wait, please. Generating %s entities" % amount)
        for i in range(amount):
            self.add_random_location()
            self.add_random_charging_station()
            self.add_random_plug()
            self.add_random_customer()
            self.add_random_car_type()
            self.add_random_car_part()
            self.add_random_workshop()
            self.add_random_workshop_car_part()
            self.add_random_provider()
            self.add_random_provide_car_parts()
            self.add_random_car()
            self.add_random_ride()
            self.add_random_charge()
            self.add_random_repair()
            print("Generate %s entities" % (i + 1))
        print("Done. Thanks for waiting")
