select
	avg(total_distance) as avg_distance,
	stddev(total_distance) as std_distance,
	avg(packages) as avg_packages,
	stddev(packages) as std_packages,
	avg(delivered_packages) as avg_delivered_packages,
	stddev(delivered_packages) as std_delivered_packages,
	avg(real_completion_time) as avg_real_completion_time,
	stddev(real_completion_time) as std_real_completion_time,
	avg(pickup_distance) as avg_pickup_distance,
	stddev(pickup_distance) as std_pickup_distance,
	avg(pickup_time) as avg_pickup_time,
	stddev(pickup_time) as std_pickup_time,
	avg(check_in_time) as avg_check_in_time,
	stddev(check_in_time) as std_check_in_time
from itineraries