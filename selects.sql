-- 1
select car.plate from car
join ride on car.plate = ride.plate
where color = 'Red' and car.plate like 'AN%' and username = 'Day7';  -- example

-- 2
select charged_datetime from charge
join charging_station on charge.UID = charging_station.UID
where charge.UID = 4299950248 and charged_datetime like '2018-05-06%'; -- example

-- 3
select using_start, using_end from ride
where using_start BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime');

-- 4
select charged_datetime from charge
join ride on charge.plate = ride.plate
where (cast(((julianday('now') - julianday(charged_datetime))/(365/12)) as integer) < 1) and (username = 'Day7') -- example
order by charged_datetime;

-- 5
select using_start, using_end, coordinate_a, coordinate_b from ride
where using_start = '2018-11-20'; -- example

-- 6
select strftime('%H', using_start), coordinate_a, coordinate_b from ride
where (cast(strftime('%H', using_start) as integer)>= 7 and (cast(strftime('%H', using_start) as integer) <= 10))
   or (cast(strftime('%H', using_start) as integer)>= 12 and (cast(strftime('%H', using_start) as integer) <= 14))
   or (cast(strftime('%H', using_start) as integer)>= 17 and (cast(strftime('%H', using_start) as integer) <= 19));

-- 7
select car.plate from car
join ride on car.plate = ride.plate
where (cast(strftime('%H', using_start) as integer)>= 7 and (cast(strftime('%H', using_start) as integer) <= 10))
   or (cast(strftime('%H', using_start) as integer)>= 12 and (cast(strftime('%H', using_start) as integer) <= 14))
   or (cast(strftime('%H', using_start) as integer)>= 17 and (cast(strftime('%H', using_start) as integer) <= 19))
order by car.plate;

-- 8
select ride.username from ride
join charge on ride.plate = charge.plate
where ((cast(((julianday('now') - julianday(ride.using_start))/(365/12)) as integer) < 1)
   and (cast(strftime('%d', using_start) as integer) = cast(strftime('%d', charged_datetime) as integer)))
order by ride.username;

-- 9
select part_type, car_type, amount, WID, provided_date from provide_car_parts
