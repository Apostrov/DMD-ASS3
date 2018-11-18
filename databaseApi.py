import sqlite3


class CarSharingDataBase():
    conn = sqlite3.connect('Car_sharing_service.db')
    cursor = conn.cursor()

    def __init__(self):
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
          aviable_sockets int,
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

          primary key (PID, WID),
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

          primary key (CID, username),
          foreign key (CID) references car (CID),
          foreign key (username) references customer (username)
        );
        ''')

        # Charge table
        self.cursor.execute('''
        create table if not exists charge (
          CID int not null,
          UID int not null,

          primary key (CID, UID),
          foreign key (CID) references car (CID),
          foreign key (UID) references charging_station (UID)
        );
        ''')

        # Repair table
        self.cursor.execute('''
        create table if not exists repair (
          CID int not null,
          WID int not null,

          primary key (CID, WID),
          foreign key (CID) references car (CID)
        );
        ''')

        self.conn.commit()

    def add_location(self, GPS, city, street, zip_code):
        vals = (GPS, city, street, zip_code)
        self.cursor.execute("insert into location values (?, ?, ?, ?)", vals)
        self.conn.commit()

    def add_charging_station(self, UID, aviable_sockets, price, time_of_charging, GPS):
        vals = (UID, aviable_sockets, price, time_of_charging, GPS)
        self.cursor.execute("insert into charging_station values (?, ?, ?, ?, ?)", vals)
        self.conn.commit()

    def add_plug(self, UID, shape, size):
        vals = (UID, shape, size)
        self.cursor.execute("insert into plug values (?, ?, ?)", vals)
        self.conn.commit()

    def add_customer(self, username, fullname, phone_number, email, GPS):
        vals = (username, fullname, phone_number, email, GPS)
        self.cursor.execute("insert into customer values (?, ?, ?, ?, ?)", vals)
        self.conn.commit()

    def add_workshop(self, WID, timing_availability, GPS):
        vals = (WID, timing_availability, GPS)
        self.cursor.execute("insert into workshop values (?, ?, ?)", vals)
        self.conn.commit()

    def add_car_part(self, part_type, car_part, amount, specifications, id, WID):
        vals = (part_type, car_part, amount, specifications, id, WID)
        self.cursor.execute("insert into car_part values (?, ?, ?, ?, ?, ?)", vals)
        self.conn.commit()

    def add_provider(self, phone_number, PID, GPS):
        vals = (phone_number, PID, GPS)
        self.cursor.execute("insert into provider values (?, ?, ?)", vals)
        self.conn.commit()

    def add_provide_car_parts(self, part_type, car_part, amount, specifications, PID, WID):
        vals = (part_type, car_part, amount, specifications, PID, WID)
        self.cursor.execute("insert into provide_car_parts values (?, ?, ?, ?, ?, ?)", vals)
        self.conn.commit()

    def add_car(self, CID, type, broken, charge_amount, GPS):
        vals = (CID, type, broken, charge_amount, GPS)
        self.cursor.execute("insert into car values (?, ?, ?, ?, ?)", vals)
        self.conn.commit()

    def add_ride(self, CID, username, coordinate_a, coordinate_b):
        vals = (CID, username, coordinate_a, coordinate_b)
        self.cursor.execute("insert into ride values (?, ?, ?, ?)", vals)
        self.conn.commit()

    def add_charge(self, CID, UID):
        vals = (CID, UID)
        self.cursor.execute("insert into charge values (?, ?)", vals)
        self.conn.commit()

    def add_repair(self, CID, WID):
        vals = (CID, WID)
        self.cursor.execute("insert into repair values (?, ?)", vals)
        self.conn.commit()


if __name__ == '__main__':
    db = CarSharingDataBase()
    db.add_location("123'456 e 2323'433", "Real City", "Leninskaya", "445223")
