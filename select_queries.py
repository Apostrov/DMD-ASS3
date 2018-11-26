import datetime
from database_api import CarSharingDataBase


def increment_value_dict(key, dictionary, value):
    if key not in dictionary.keys():
        dictionary[key] = 0
    dictionary[key] += value
    return dictionary


# First Query
def find_car(db, color, plate, username, day):
    vals = (color, plate + "%", username, day)
    db.execute_query('''
    select car.plate 
    from car
        natural join ride
    where color = ? 
        and car.plate like ? 
        and username = ? 
        and using_start >= ?
    ''', vals)
    plates = [x[0] for x in db.get_answer()]
    return plates


# Second Query
def number_sockets_occupied(db, uid, date):
    vals = (uid, date)
    db.execute_query('''
    select strftime('%H', charged_datetime) 
    from charge
        natural join charging_station
    where charge.UID = ? and date(charged_datetime) = ?
    ''', vals)
    hours = [int(x[0]) for x in db.get_answer()]
    occupied = []
    for hour in range(24):
        occupied.append(hours.count(hour))

    return occupied


# Third Query
def week_statistic(db):
    db.execute_query('''
    select strftime('%H', using_start), strftime('%H', using_end) 
    from ride
    where using_start between datetime('now', '-6 days') and datetime('now', 'localtime');
    ''')
    car_times = db.get_answer()
    cars_duringtime = [0, 0, 0]  # morning (7AM - 10 AM), afternoon (12AM - 2PM) and evening (5PM - 7PM)
    for time in car_times:
        if (7 <= int(time[0]) <= 10) or (7 <= int(time[1]) <= 10):
            cars_duringtime[0] += 1
        if (12 <= int(time[0]) <= 14) or (12 <= int(time[1]) <= 14):
            cars_duringtime[1] += 1
        if (17 <= int(time[0]) <= 19) or (17 <= int(time[1]) <= 19):
            cars_duringtime[2] += 1
    cars_amount = len(db.select_table_column('car', 'plate'))
    if cars_amount == 0:
        return [0, 0, 0]
    cars_duringtime = [int(x / cars_amount * 100) for x in cars_duringtime]
    return cars_duringtime


# Fourth Query
def twice_charge(db, username):
    vals = (username,)
    db.execute_query('''
    select charged_datetime, count(charged_datetime)
    from ride
          natural join charge
    where username = ?
        and charged_datetime between using_start and using_end;
    ''', vals)
    charge_count = db.get_answer()
    if int(charge_count[0][1]) >= 2:
        return charge_count[0][0]
    return 0


# Fifth Query
def ride_statistic(db, day):
    vals = (day,)
    db.execute_query('''
    select using_start, using_end, coordinate_a, coordinate_b 
    from ride
    where date(using_start) = ?
    ''', vals)
    times_and_coordinates = db.get_answer()
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
def popular_travel(db):
    db.execute_query('''
    select strftime('%H', using_start), coordinate_a, coordinate_b
    from ride
    where (cast(strftime('%H', using_start) as integer) >= 7 and (cast(strftime('%H', using_start) as integer) <= 10))
        or (cast(strftime('%H', using_start) as integer) >= 12 and (cast(strftime('%H', using_start) as integer) <= 14))
        or (cast(strftime('%H', using_start) as integer) >= 17 and (cast(strftime('%H', using_start) as integer) <= 19))
    ''')

    time_and_coordinates = db.get_answer()
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
def delete_car_ten_percentage(db):
    db.execute_query('''
    select plate, count(using_start)
    from ride
    where using_start between datetime('now', '-91 days') and datetime('now', 'localtime')
    group by plate
    union
    select plate, 0
    from car
    order by count(using_start);
    ''')

    plate_counts = db.get_answer()
    count_dict = {}
    for pc in plate_counts:
        if pc not in count_dict:
            count_dict[pc[0]] = 0
        count_dict[pc[0]] += pc[1]
    count = 0
    max_count = round(0.1 * len(count_dict))
    for plate in sorted(count_dict, key=count_dict.get):
        db.delete_by_condition('car', "plate = '" + plate + "'")
        count += 1
        if count == max_count:
            return


# Eighth Query
def charge_amount(db, starting_date):
    vals = (starting_date,)
    db.execute_query('''
    select username, count(charged_datetime)
    from ride
          natural join charge
    where date(using_start) >= ? -- example
    group by username;
    ''', vals)

    charges = db.get_answer()
    return charges


# Ninth Query
def often_require_car_part(db):
    db.execute_query('''
    select part_ID, WID, amount, provided_date 
    from provide_car_parts
    ''')
    provided_car_parts = db.get_answer()
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
    db.execute_query('''
    select part_ID, part_type, car_type 
    from car_part
    where part_ID in ''' + str(tuple(vals)))

    part_info = db.cursor.fetchall()
    return require_car_part, part_info


# Tenth Query
def car_with_expensive_service(db):
    db.execute_query('''
    select car_type, cost, purchase_date 
    from repair
        natural join (select plate, car_type, purchase_date from car);
    ''')

    repair_costs = db.get_answer()
    waste_money = {}
    for rc in repair_costs:
        if rc[0] not in waste_money:
            waste_money[rc[0]] = {'cost': 0, 'number': 0}
        day_passed = (datetime.datetime.now() - datetime.datetime.strptime(rc[2], '%Y-%m-%d')).days
        waste_money[rc[0]]['cost'] += rc[1] / day_passed
        waste_money[rc[0]]['number'] += 1

    db.execute_query('''
    select car_type, cost, purchase_date 
    from charge
        natural join (select plate, car_type, purchase_date from car);
    ''')

    charge_costs = db.get_answer()
    for rc in charge_costs:
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


def sample_start(db):
    db.recreate_all_tables()
    db.add_random_data(20)

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
    # sample_start(db)
    # Query
    print(find_car(db, "Red", "AN", "Day7", "2018-11-20"))
    print(number_sockets_occupied(db, 1, "2018-11-20"))
    print(week_statistic(db))
    print(ride_statistic(db, '2018-11-20'))
    print(popular_travel(db))
    print(often_require_car_part(db))
    print(car_with_expensive_service(db))
    delete_car_ten_percentage(db)
    print(charge_amount(db, '2017.10.01'))
    print(twice_charge(db, "Day7"))
    db.close_db()
