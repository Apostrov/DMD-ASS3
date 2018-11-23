-- 2
select charged_datetime from charge
join charging_station on charge.UID == charging_station.UID
where charge.UID == 2 and charged_datetime >= '2018-2-1' and charged_datetime < '2018-3-1' -- example