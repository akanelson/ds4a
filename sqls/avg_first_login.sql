select subquery.driver_id, to_char(avg(subquery.hora), 'HH24:MI:SS') as FirstLogin into firstlogin 
from 
(select driver_id, Date(sent) AS Fecha, min((sent) ::timestamp::time) AS Hora
from availabilities
group by 1,2
order by driver_id, fecha) as subquery
group by driver_id