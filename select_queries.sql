-- 1
select car.plate from car
join ride on car.plate = ride.plate
where color = 'Red' and car.plate like 'AN%' and username = 'Day7';  -- example

-- 2
select charged_datetime from charge
join charging_station on charge.UID == charging_station.UID
where charge.UID = 4299950248 and charged_datetime like '2018-05-06%'; -- example

-- 3
select using_start, using_end from ride
where using_start BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime');