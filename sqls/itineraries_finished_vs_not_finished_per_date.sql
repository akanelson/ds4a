select
	*,
	round(cast(finished as numeric)/cast(total as numeric), 2) as finished_ratio,
	round(cast(not_finished as numeric)/cast(total as numeric), 2) as not_finished_ratio
from
	(select
		date(created) as created_date,
		sum(case when status='finished' then 1 else 0 end) as finished,
		sum(case when status<>'finished' then 1 else 0 end) as not_finished,
	    sum(1) as total
	from itineraries
	group by date(created)
	) t
/* where total = 0	 */
order by created_date
limit 10