import sqlite3
import random
import string


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
    def add_workshop(self, WID, timing_availability, GPS):
        vals = (WID, timing_availability, GPS)
        self.execute_query("insert into workshop values (?, ?, ?)", vals)

    def add_random_workshop(self):
        all_gps = self.select_table_column("location", "GPS")
        if len(all_gps) < 1:
            return

        WID = generate_random_int(10)
        timing_availability = "00:00:" + generate_random_int(2)
        GPS = random.choice(all_gps)[0]

        self.add_workshop(WID, timing_availability, GPS)

    # Car part
    def add_car_part(self, part_type, car_part, amount, specifications, id, WID):
        vals = (part_type, car_part, amount, specifications, id, WID)
        self.execute_query("insert into car_part values (?, ?, ?, ?, ?, ?)", vals)

    def add_random_car_part(self):
        all_wid = self.select_table_column("workshop", "WID")
        if len(all_wid) < 1:
            return

        part_type = generate_random_string(40)
        car_type = generate_random_string(40)
        amount = generate_random_string(40)
        specifications = generate_random_string(100)
        id = generate_random_int(10)
        WID = random.choice(all_wid)[0]

        self.add_car_part(part_type, car_type, amount, specifications, id, WID)

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
        amount = generate_random_string(40)
        specifications = generate_random_string(100)
        PID = random.choice(all_pid)[0]
        WID = random.choice(all_wid)[0]

        self.add_provide_car_parts(part_type, car_type, amount, specifications, PID, WID)

    # Car
    def add_car(self, CID, type, broken, charge_amount, GPS):
        vals = (CID, type, broken, charge_amount, GPS)
        self.execute_query("insert into car values (?, ?, ?, ?, ?)", vals)

    def add_random_car(self):
        CID = generate_random_int(10)
        type = generate_random_string(50)
        broken = False
        charge_amount = generate_random_int(2)
        GPS = generate_random_string(50)

        self.add_car(CID, type, broken, charge_amount, GPS)

    # Ride
    def add_ride(self, CID, username, coordinate_a, coordinate_b):
        vals = (CID, username, coordinate_a, coordinate_b)
        self.execute_query("insert into ride values (?, ?, ?, ?)", vals)

    def add_random_ride(self):
        all_cid = self.select_table_column("car", "CID")
        if len(all_cid) < 1:
            return

        all_username = self.select_table_column("customer", "username")
        if len(all_username) < 1:
            return

        coordinate_a = generate_random_string(50)
        coordinate_b = generate_random_string(50)
        CID = random.choice(all_cid)[0]
        username = random.choice(all_username)[0]

        self.add_ride(CID, username, coordinate_a, coordinate_b)

    # Charge
    def add_charge(self, CID, UID, datetime):
        vals = (CID, UID, datetime)
        self.execute_query("insert into charge values (?, ?, ?)", vals)

    def add_random_charge(self):
        all_cid = self.select_table_column("car", "CID")
        if len(all_cid) < 1:
            return

        all_uid = self.select_table_column("charging_station", "UID")
        if len(all_uid) < 1:
            return

        CID = random.choice(all_cid)[0]
        UID = random.choice(all_uid)[0]
        datetime = generate_random_date() + " " + generate_random_time()

        self.add_charge(CID, UID, datetime)

    # Repair
    def add_repair(self, CID, WID):
        vals = (CID, WID)
        self.execute_query("insert into repair values (?, ?)", vals)

    def add_random_repair(self):
        all_cid = self.select_table_column("car", "CID")
        if len(all_cid) < 1:
            return

        all_wid = self.select_table_column("workshop", "WID")
        if len(all_wid) < 1:
            return

        CID = random.choice(all_cid)[0]
        WID = random.choice(all_wid)[0]

        self.add_repair(CID, WID)

    # Select Queries
    def first_query(self):
        pass

    def number_sockets_occupied(self, uid, date):
        vals = (uid, date + "%")
        self.execute_query('''
        select strftime('%H', charged_datetime) from charge
        join charging_station on charge.UID == charging_station.UID
        where charge.UID = ? and charged_datetime like ?
        ''', vals)
        hours = [int(x[0]) for x in self.cursor.fetchall()]
        occupied = []
        for hour in range(24):
            occupied.append(hours.count(hour))

        return occupied

    # Another func
    # May take a long time ((
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
    print(db.number_sockets_occupied('2338107531', '2018-02-05'))
    db.close_db()
