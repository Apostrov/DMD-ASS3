--1
SELECT * FROM car
WHERE color = 'Red' and plate LIKE 'AN%'

--3
SELECT using_start, using_end FROM ride

--5
SELECT using_start, using_end, coordinate_a, coordinate_b FROM ride

--6
SELECT using_start, coordinate_a, coordinate_b FROM ride
WHERE using_start [TIME] [HOUR] (>= 7 AND <= 10) OR (>=12 AND <=14) OR (>=17 AND <=19)

--