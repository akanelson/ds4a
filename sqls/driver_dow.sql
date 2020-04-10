/* Create drivers table for Day Of the Week analysis */
/* Sunday is 0 */
CREATE TABLE driver_dow AS
	SELECT  driver_id,
			EXTRACT(DOW FROM sent) as dow,
			COUNT(1) AS pushes,
			COUNT(DISTINCT(itinerary_id)) as itineraries,
			AVG(lat) as avg_lat,
			AVG(lng) as avg_lng,
			STDDEV(lat) as std_lat,
			STDDEV(lng) as std_lng,
			MIN(EXTRACT(HOUR FROM sent)) AS min_hour,
			MAX(EXTRACT(HOUR FROM sent)) AS max_hour,
			AVG(EXTRACT(HOUR FROM sent)) AS avg_hour,
			STDDEV(EXTRACT(HOUR FROM sent)) AS std_hour
	FROM availabilities
	GROUP BY driver_id, EXTRACT(DOW FROM sent)
