-- 10
select charge.cost as ccost, repair.cost as rcost, type, charged_datetime, repaired_datetime
from charge
join repair on charge.CID == repair.CID
join car on charge.CID == car.CID