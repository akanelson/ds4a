select
	avg(total_distance), stddev(total_distance),
	avg(packages), stddev(packages),
	avg(delivered_packages), stddev(delivered_packages),
	avg(real_completion_time), stddev(real_completion_time),
	avg(pickup_distance), stddev(pickup_distance),	
	avg(pickup_time), stddev(pickup_time),
	avg(check_in_time), stddev(check_in_time),
	avg(pickup_time), stddev(pickup_time)
from itineraries