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

-- 5
select using_start, using_end, coordinate_a, coordinate_b from ride
where using_start = '2018-11-20'; -- example

-- 6
select strftime('%H', using_start), coordinate_a, coordinate_b from ride
where (cast(strftime('%H', using_start) as integer)>= 7 and (cast(strftime('%H', using_start) as integer) <= 10))
   or (cast(strftime('%H', using_start) as integer)>= 12 and (cast(strftime('%H', using_start) as integer) <= 14))
   or (cast(strftime('%H', using_start) as integer)>= 17 and (cast(strftime('%H', using_start) as integer) <= 19));

-- 9
select * from provide_car_parts
