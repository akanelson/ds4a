select
	total,
	agency_1,
	round(cast(agency_1 as numeric)*100/cast(total as numeric), 2) as agency_1_percent,
	agency_2,
	round(cast(agency_2 as numeric)*100/cast(total as numeric), 2) as agency_1_percent
from
	(select
		count(1) as total,
		sum(
			case
				when distribution_center=1 then 1 else 0
			end
		) as agency_1,
		sum(
			case
				when distribution_center=2 then 1 else 0
			end
		) as agency_2
	 from availabilities) as t