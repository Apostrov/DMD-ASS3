import sqlite3
import random
import string


def generate_random_int(length):
    return ''.join(random.choices(string.digits, k=length))


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class CarSharingDataBase:
    conn = sqlite3.connect('Car_sharing_service.db')
    cursor = conn.cursor()

    def open_db(self):
        self.conn = sqlite3.connect('Car_sharing_service.db')
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.conn.commit()
        self.conn.close()

    def __init__(self):
        self.open_db()
        # Location table
        self.cursor.execute('''
        create table if not exists location (
          GPS varchar (100) not null,
          city varchar (50),
          street varchar (50),
          zip_code int,

          primary key (GPS)
        );
        ''')

        # Charging station table
        self.cursor.execute('''
        create table if not exists charging_station (
          UID int not null,
          available_sockets int,
          price varchar (50),
          time_of_charging int,
          GPS varchar (100) not null,
          
          primary key (UID),
          foreign key (GPS) references location (GPS)
        );
        ''')

        # Plug table
        self.cursor.execute('''
        create table if not exists plug (
          UID int not null,
          shape varchar (50),
          size int,

          foreign key (UID) references charging_station (UID)
        );
        ''')

        # Customer table
        self.cursor.execute('''
        create table if not exists customer (
          username varchar (50) not null,
          fullname varchar (100),
          phone_number varchar (20),
          email varchar (60),
          GPS varchar (100) not null,

          primary key (username),
          foreign key (GPS) references location (GPS)
        );
        ''')

        # Workshop table
        self.cursor.execute('''
        create table if not exists workshop (
          WID int not null,
          timing_availability time,
          GPS varchar (100) not null,

          primary key (WID),
          foreign key (GPS) references location (GPS)
        );
        ''')

        # Car Part table
        self.cursor.execute('''
        create table if not exists car_part (
          part_type varchar (40),
          car_type varchar (40),
          amount varchar (40),
          specifications varchar (150),
          id int not null,
          WID int not null,

          primary key (id),
          foreign key (WID) references workshop (WID)
        );
        ''')

        # Provider table
        self.cursor.execute('''
        create table if not exists provider (
          phone_number varchar (20),
          PID int not null,
          GPS varchar (100) not null,

          primary key (PID),
          foreign key (gps) references location (GPS)
        );
        ''')

        # Provide car parts table
        self.cursor.execute('''
        create table if not exists provide_car_parts (
          part_type varchar (40),
          car_type varchar (40),
          amount varchar (40),
          specifications varchar (150),
          PID int not null,
          WID int not null,

          foreign key (PID) references provider (PID),
          foreign key (WID) references workshop (WID)
        );
        ''')

        # Car table
        self.cursor.execute('''
        create table if not exists car (
          CID int not null,
          type varchar (50),
          broken boolean,
          charge_amount int,
          GPS varchar (100),

          primary key (CID)
        );
        ''')

        # Ride table
        self.cursor.execute('''
        create table if not exists ride (
          CID int not null,
          username varchar (50) not null,
          coordinate_a varchar (100),
          coordinate_b varchar (100),

          foreign key (CID) references car (CID),
          foreign key (username) references customer (username)
        );
        ''')

        # Charge table
        self.cursor.execute('''
        create table if not exists charge (
          CID int not null,
          UID int not null,

          foreign key (CID) references car (CID),
          foreign key (UID) references charging_station (UID)
        );
        ''')

        # Repair table
        self.cursor.execute('''
        create table if not exists repair (
          CID int not null,
          WID int not null,

          foreign key (CID) references car (CID),
          foreign key (WID) references workshop (WID)
        );
        ''')

        self.conn.commit()

    # !!! Not secured from sql injection
    def select_table_column(self, table, column='*'):
        self.cursor.execute('select %s from %s' % (column, table))
        return self.cursor.fetchall()

    def execute_custom_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    # Location
    def add_location(self, GPS, city, street, zip_code):
        vals = (GPS, city, street, zip_code)
        self.cursor.execute("insert into location values (?, ?, ?, ?)", vals)
        self.conn.commit()

    def add_random_location(self):
        GPS = generate_random_string(50)
        city = generate_random_string(50)
        street = generate_random_string(50)
        zip_code = generate_random_int(20)
        self.add_location(GPS, city, street, zip_code)

    # Charging station
    def add_charging_station(self, UID, available_sockets, price, time_of_charging, GPS):
        vals = (UID, available_sockets, price, time_of_charging, GPS)
        self.cursor.execute("insert into charging_station values (?, ?, ?, ?, ?)", vals)
        self.conn.commit()

    def add_random_charging_station(self):
        all_gps = self.select_table_column("location", "GPS")
        if len(all_gps) < 1:
            return

        UID = generate_random_int(20)
        available_sockets = generate_random_int(2)
        price = generate_random_string(3)
        time_of_charging = generate_random_int(2)
        GPS = random.choice(all_gps)[0]
        self.add_charging_station(UID, available_sockets, price, time_of_charging, GPS)

    # Plug
    def add_plug(self, UID, shape, size):
        vals = (UID, shape, size)
        self.cursor.execute("insert into plug values (?, ?, ?)", vals)
        self.conn.commit()

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
        self.cursor.execute("insert into customer values (?, ?, ?, ?, ?)", vals)
        self.conn.commit()

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
        self.cursor.execute("insert into workshop values (?, ?, ?)", vals)
        self.conn.commit()

    def add_random_workshop(self):
        all_gps = self.select_table_column("location", "GPS")
        if len(all_gps) < 1:
            return

        WID = generate_random_int(20)
        timing_availability = "00:00:" + generate_random_int(2)
        GPS = random.choice(all_gps)[0]

        self.add_workshop(WID, timing_availability, GPS)

    # Car part
    def add_car_part(self, part_type, car_part, amount, specifications, id, WID):
        vals = (part_type, car_part, amount, specifications, id, WID)
        self.cursor.execute("insert into car_part values (?, ?, ?, ?, ?, ?)", vals)
        self.conn.commit()

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
        self.cursor.execute("insert into provider values (?, ?, ?)", vals)
        self.conn.commit()

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
        self.cursor.execute("insert into provide_car_parts values (?, ?, ?, ?, ?, ?)", vals)
        self.conn.commit()

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
        self.cursor.execute("insert into car values (?, ?, ?, ?, ?)", vals)
        self.conn.commit()

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
        self.cursor.execute("insert into ride values (?, ?, ?, ?)", vals)
        self.conn.commit()

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
    def add_charge(self, CID, UID):
        vals = (CID, UID)
        self.cursor.execute("insert into charge values (?, ?)", vals)
        self.conn.commit()

    def add_random_charge(self):
        all_cid = self.select_table_column("car", "CID")
        if len(all_cid) < 1:
            return

        all_uid = self.select_table_column("charging_station", "UID")
        if len(all_uid) < 1:
            return

        CID = random.choice(all_cid)[0]
        UID = random.choice(all_uid)[0]

        self.add_charge(CID, UID)

    # Repair
    def add_repair(self, CID, WID):
        vals = (CID, WID)
        self.cursor.execute("insert into repair values (?, ?)", vals)
        self.conn.commit()

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

    # Another func
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
    db.add_random_data(5)
    db.close_db()
