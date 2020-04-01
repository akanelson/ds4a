/* Build a table with the whole available drivers find in table availables */
CREATE TABLE driver AS
	SELECT driver_id,
	    distribution_center,
		MIN(sent) AS min_sent,
		MAX(sent) AS max_sent,
		COUNT(1) AS pushes
	FROM availabilities
	GROUP BY driver_id, distribution_center;


/* Create table to analyze WTF is happening with our datesets */
CREATE TABLE wtf AS
	SELECT
		COUNT(DISTINCT(driver.itinerary_id )) AS av_itineraries_id,
		COUNT(DISTINCT(i.itinerary_id)) AS it_itineraries_id,
		driver.driver_id
	FROM availabilities driver
	INNER JOIN itineraries i ON driver.driver_id = i.driver_id 
	WHERE driver.itinerary_id IS NOT NULL 
	AND sent > '2019-10-01'
	GROUP BY driver.driver_id ;

/* We expect that the unique number of itineraries for a driver is
the same in the same date range, but this doesn't happen */
SELECT *, ABS(av_itineraries_id-it_itineraries_id) AS d
FROM wtf
ORDER BY d DESC
LIMIT 20;

/* We can see a special case. This driver has many itineraries assigned in
the availability dataset but just a few in the itinerary. And what makes it
even worst, is that itinerary_ids do not match */

/* This driver has 3 unique itinerary_id in itineraries dataset */
SELECT COUNT(itinerary_id)
FROM itineraries
WHERE driver_id = '4202df1487b9fd6030280541626beee8'

/* The same driver has 945 unique itinerary_id in availabilities dataset */
SELECT COUNT(DISTINCT(itinerary_id))
FROM availabilities
WHERE driver_id = '4202df1487b9fd6030280541626beee8'
AND itinerary_id IS NOT NULL

/* In itineraries dataset there exist only 4 itinerary_id of these 945 */

/* And 2 of them belong to other drivers */
SELECT  COUNT(DISTINCT(itinerary_id)) as itineraries,
		COUNT(DISTINCT(driver_id)) as drivers,
		SUM(CASE
			WHEN driver_id='4202df1487b9fd6030280541626beee8'
			THEN 1 ELSE 0
			END) AS from_our_driver 
FROM itineraries i
WHERE i.itinerary_id in
	(SELECT
		distinct(itinerary_id)
	FROM availabilities
	WHERE driver_id = '4202df1487b9fd6030280541626beee8'
	AND itinerary_id IS NOT NULL)
	
