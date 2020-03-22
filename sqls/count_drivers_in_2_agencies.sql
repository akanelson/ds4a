select count(driver_id) as drivers_in_2_agencies
from
	(
	select
		driver_id, count(distinct(distribution_center1)) as agencies
	from itineraries
	group by driver_id
	) a
where agencies = 2