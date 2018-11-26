-- 1
select car.plate
from car
       natural join ride
where color = 'Red'
  and car.plate like 'AN%'
  and username = 'Day7'
  and using_start >= '2018-05-06'; -- example

-- 2
select charged_datetime
from charge
       natural join charging_station
where charge.UID = 4299950248
  and date(charged_datetime) = '2018-05-06'; -- example

-- 3
select using_start, using_end
from ride
where using_start between datetime('now', '-6 days') and datetime('now', 'localtime');

-- 5
select using_start, using_end, coordinate_a, coordinate_b
from ride
where using_start = '2018-11-20'; -- example

-- 6
select strftime('%H', using_start), coordinate_a, coordinate_b
from ride
where (cast(strftime('%H', using_start) as integer) >= 7 and (cast(strftime('%H', using_start) as integer) <= 10))
   or (cast(strftime('%H', using_start) as integer) >= 12 and (cast(strftime('%H', using_start) as integer) <= 14))
   or (cast(strftime('%H', using_start) as integer) >= 17 and (cast(strftime('%H', using_start) as integer) <= 19));

-- 7
select plate, count(using_start)
from ride
where using_start BETWEEN datetime('now', '-91 days') AND datetime('now', 'localtime')
group by plate
union
select plate, 0
from car
order by count(using_start);

-- 8
select ride.username
from ride
       join charge on ride.plate = charge.plate
where ((cast(((julianday('now') - julianday(ride.using_start)) / (365 / 12)) as integer) < 1)
  and (cast(strftime('%d', using_start) as integer) = cast(strftime('%d', charged_datetime) as integer)))
order by ride.username;

-- 9
select amount, part_ID, WID, provided_date
from provide_car_parts;

-- 10
select car_type, cost, purchase_date
from repair
       natural join (select plate, car_type, purchase_date from car);

select car_type, cost, purchase_date
from charge
       natural join (select plate, car_type, purchase_date from car);
