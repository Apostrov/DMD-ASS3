import sqlite3
import random
import string
import datetime


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


def increment_value_dict(key, dictionary, value):
    if key not in dictionary.keys():
        dictionary[key] = 0
    dictionary[key] += value
    return dictionary


class CarSharingDataBase:
    conn = sqlite3.connect('Car_sharing_service.db')
    cursor = conn.cursor()

    def open_db(self):
        self.conn = sqlite3.connect('Car_sharing_service.db')
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.conn.commit()
        self.conn.close()

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
        print('delete from %s where %s' % (table, delete_condition))
        self.execute_query('delete from %s where %s' % (table, delete_condition))

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
        GPS = generate_random_string(50)
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

        coordinate_a = generate_random_string(50)
        coordinate_b = generate_random_string(50)
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

    # Select Queries
    # First Query
    def find_car(self, color, plate, username, day):
        vals = (color, plate + "%", username, day)
        self.execute_query('''
        select car.plate 
        from car
            natural join ride
        where color = ? 
            and car.plate like ? 
            and username = ? 
            and using_start >= ?
        ''', vals)
        plates = [x[0] for x in self.cursor.fetchall()]
        return plates

    # Second Query
    def number_sockets_occupied(self, uid, date):
        vals = (uid, date)
        self.execute_query('''
        select strftime('%H', charged_datetime) 
        from charge
            natural join charging_station
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
        select strftime('%H', using_start), strftime('%H', using_end) 
        from ride
        where using_start between datetime('now', '-6 days') and datetime('now', 'localtime');
        ''')
        car_times = self.cursor.fetchall()
        cars_duringtime = [0, 0, 0]  # morning (7AM - 10 AM), afternoon (12AM - 2PM) and evening (5PM - 7PM)
        for time in car_times:
            if (7 <= int(time[0]) <= 10) or (7 <= int(time[1]) <= 10):
                cars_duringtime[0] += 1
            if (12 <= int(time[0]) <= 14) or (12 <= int(time[1]) <= 14):
                cars_duringtime[1] += 1
            if (17 <= int(time[0]) <= 19) or (17 <= int(time[1]) <= 19):
                cars_duringtime[2] += 1
        cars_amount = len(self.select_table_column('car', 'plate'))
        if cars_amount == 0:
            return [0, 0, 0]
        cars_duringtime = [int(x / cars_amount * 100) for x in cars_duringtime]
        return cars_duringtime

    # Fourth Query
    def fourt(self):
        pass

    # Fifth Query
    def ride_statistic(self, day):
        vals = (day,)
        self.execute_query('''
        select using_start, using_end, coordinate_a, coordinate_b 
        from ride
        where date(using_start) = ?
        ''', vals)
        times_and_coordinates = self.cursor.fetchall()
        durations = []
        for tandc in times_and_coordinates:
            time_start = datetime.datetime.strptime(tandc[0], '%Y-%m-%d %H:%M:%S')
            time_end = datetime.datetime.strptime(tandc[1], '%Y-%m-%d %H:%M:%S')
            durations.append(time_end - time_start)
        if len(durations) == 0:
            return 0
        average_time = sum([x.seconds for x in durations]) / len(durations)
        return average_time

    # Sixth Query
    def popular_travel(self):
        self.execute_query('''
        select strftime('%H', using_start), coordinate_a, coordinate_b
        from ride
        where (cast(strftime('%H', using_start) as integer) >= 7 and (cast(strftime('%H', using_start) as integer) <= 10))
            or (cast(strftime('%H', using_start) as integer) >= 12 and (cast(strftime('%H', using_start) as integer) <= 14))
            or (cast(strftime('%H', using_start) as integer) >= 17 and (cast(strftime('%H', using_start) as integer) <= 19))
        ''')

        time_and_coordinates = self.cursor.fetchall()
        morning_pickups = {}
        morning_travelpoints = {}

        afternoon_pickups = {}
        afternoon_travelpoints = {}

        evening_pickups = {}
        evening_travelpoints = {}

        for tandc in time_and_coordinates:
            if 7 <= int(tandc[0]) <= 10:
                morning_pickups = increment_value_dict(tandc[1], morning_pickups, 1)
                morning_travelpoints = increment_value_dict(tandc[2], morning_travelpoints, 1)
            if 12 <= int(tandc[0]) <= 14:
                afternoon_pickups = increment_value_dict(tandc[1], afternoon_pickups, 1)
                afternoon_travelpoints = increment_value_dict(tandc[2], afternoon_travelpoints, 1)
            if 17 <= int(tandc[0]) <= 19:
                evening_pickups = increment_value_dict(tandc[1], evening_pickups, 1)
                evening_travelpoints = increment_value_dict(tandc[2], evening_travelpoints, 1)

        return [sorted(morning_pickups, key=morning_pickups.get, reverse=True)[:3],
                sorted(morning_travelpoints, key=morning_travelpoints.get, reverse=True)[:3],
                sorted(afternoon_pickups, key=afternoon_pickups.get, reverse=True)[:3],
                sorted(afternoon_travelpoints, key=afternoon_travelpoints.get, reverse=True)[:3],
                sorted(evening_pickups, key=evening_pickups.get, reverse=True)[:3],
                sorted(evening_travelpoints, key=evening_travelpoints.get, reverse=True)[:3]]

    # Seventh Query
    def delete_car_ten_percentage(self):
        self.execute_query('''
        select plate, count(using_start)
        from ride
        where using_start between datetime('now', '-91 days') and datetime('now', 'localtime')
        group by plate
        union
        select plate, 0
        from car
        order by count(using_start);
        ''')

        plate_counts = self.cursor.fetchall()
        count_dict = {}
        for pc in plate_counts:
            if pc not in count_dict:
                count_dict[pc[0]] = 0
            count_dict[pc[0]] += pc[1]
        count = 0
        max_count = round(0.1 * len(count_dict))
        for plate in sorted(count_dict, key=count_dict.get):
            self.delete_by_condition('car', "plate = '" + plate + "'")
            count += 1
            if count == max_count:
                return

    # Ninth Query
    def often_require_car_part(self):
        self.execute_query('''
        select part_ID, WID, amount, provided_date 
        from provide_car_parts
        ''')
        provided_car_parts = self.cursor.fetchall()
        wid_car_part = {}
        for pcp in provided_car_parts:
            partID = pcp[0]
            wid = pcp[1]
            amount = pcp[2]
            provide_data = datetime.datetime.strptime(pcp[3], '%Y-%m-%d')

            if wid not in wid_car_part:
                wid_car_part[wid] = {}

            if partID not in wid_car_part[wid]:
                wid_car_part[wid][partID] = {'amount': 0, "first_add_data": provide_data}

            wid_car_part[wid][partID]['amount'] += amount

            if wid_car_part[wid][partID]["first_add_data"] > provide_data:
                wid_car_part[wid][partID]["first_add_data"] = provide_data

        require_car_part = {}
        for wid in wid_car_part.keys():
            if wid not in require_car_part:
                require_car_part[wid] = {}
            for partID in wid_car_part[wid].keys():
                days = (datetime.datetime.now() - wid_car_part[wid][partID]['first_add_data']).days
                if days == 0:
                    days = 1
                amount = wid_car_part[wid][partID]['amount'] / days
                if len(require_car_part[wid]) == 0:
                    require_car_part[wid] = [partID, amount]
                elif require_car_part[wid][1] < amount:
                    require_car_part[wid] = [partID, amount]

        vals = [part[0] for part in require_car_part.values()]
        self.execute_query('''
        select part_ID, part_type, car_type 
        from car_part
        where part_ID in ''' + str(tuple(vals)))

        part_info = self.cursor.fetchall()
        return require_car_part, part_info

    # Tenth Query
    def car_with_expensive_service(self):
        self.execute_query('''
        select car_type, cost, purchase_date 
        from repair
            natural join (select plate, car_type, purchase_date from car);
        ''')

        repair_costs = self.cursor.fetchall()
        waste_money = {}
        for rc in repair_costs:
            if rc[0] not in waste_money:
                waste_money[rc[0]] = {'cost': 0, 'number': 0}
            day_passed = (datetime.datetime.now() - datetime.datetime.strptime(rc[2], '%Y-%m-%d')).days
            waste_money[rc[0]]['cost'] += rc[1] / day_passed
            waste_money[rc[0]]['number'] += 1

        self.execute_query('''
        select car_type, cost, purchase_date 
        from charge
            natural join (select plate, car_type, purchase_date from car);
        ''')

        charge_costs = self.cursor.fetchall()
        for rc in repair_costs:
            if rc[0] not in waste_money:
                waste_money[rc[0]] = {'cost': 0, 'number': 0}
            day_passed = (datetime.datetime.now() - datetime.datetime.strptime(rc[2], '%Y-%m-%d')).days
            waste_money[rc[0]]['cost'] += rc[1] / day_passed
            waste_money[rc[0]]['number'] += 1

        car_type_spender = {'name': '', 'amount': 0}
        for name, wasted in waste_money.items():
            amount = wasted['cost'] / wasted['number']
            if car_type_spender['amount'] < amount:
                car_type_spender['name'] = name
                car_type_spender['amount'] = amount
        return car_type_spender


def sample_start():
    db.recreate_all_tables()
    db.add_random_data(8)

    db.add_location("gps", "ksz", "strt", 111)
    db.add_charging_station(5, "10$", 10, "gps")
    db.add_plug(1, "shp", 10)
    db.add_customer("Day7", "7", "77", "777", "7777")
    db.add_car_type("B")
    db.add_car_part("part", "B", "spec")
    db.add_workshop("06:00:00", "20:00:00", "gps")
    db.add_workshop_car_part(100, 1, 2)
    db.add_provider("phone_numb", "gps")
    db.add_provide_car_parts(120, 1, 1, 1, "2018-11-19")
    db.add_car("AN123", "B", False, 100, "gps1", "Red", "2017-10-10")
    db.add_ride("AN123", "Day7", "gps1", "gps", "2018-11-20 07:00:00", "2018-11-20 08:30:00")
    db.add_charge("AN123", 1, 6, "2018-11-20 09:00:00")
    db.add_repair("AN123", 1, 20, "2018-10-31")


if __name__ == '__main__':
    db = CarSharingDataBase()
    # sample_start()
    # Query
    print(db.find_car("Red", "AN", "Day7", "2018-11-20"))
    print(db.number_sockets_occupied(1, "2018-11-20"))
    print(db.week_statistic())
    print(db.ride_statistic('2018-11-20'))
    print(db.popular_travel())
    print(db.often_require_car_part())
    print(db.car_with_expensive_service())
    db.delete_car_ten_percentage()
    db.close_db()
