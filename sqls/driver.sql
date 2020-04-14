/* Build a table with the whole available drivers found in table availables */
/* Creation time required in notebook was approx 165 seconds */
CREATE TABLE driver AS
	SELECT driver_id,
		MIN(sent) AS min_sent,
		MAX(sent) AS max_sent,
		AVG(EXTRACT(HOUR FROM sent)) AS avg_hour,
		STDDEV(EXTRACT(HOUR FROM sent)) AS std_hour,
		COUNT(1) AS pushes,
		COUNT(DISTINCT(itinerary_id)) as itineraries,
		AVG(lat) as avg_lat,
		AVG(lng) as avg_lng,
		STDDEV(lat) as std_lat,
		STDDEV(lng) as std_lng
	FROM availabilities
	GROUP BY driver_id;


/* Build a table with the whole available drivers found in table availables */
/* Creation time required in notebook was approx 165 seconds */
CREATE TABLE driver AS
	SELECT driver_id,
	    distribution_center,
		MIN(sent) AS min_sent,
		MAX(sent) AS max_sent,
		AVG(EXTRACT(HOUR FROM sent)) AS avg_hour,
		STDDEV(EXTRACT(HOUR FROM sent)) AS std_hour,
		COUNT(1) AS pushes,
		COUNT(DISTINCT(itinerary_id)) as itineraries,
		AVG(lat) as avg_lat,
		AVG(lng) as avg_lng,
		STDDEV(lat) as std_lat,
		STDDEV(lng) as std_lng
	FROM availabilities
	GROUP BY distribution_center, driver_id;