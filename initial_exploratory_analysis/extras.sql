/* Create a table with driver's agency weights based on
   the number of itineraries done by the driver */
CREATE TABLE driver_weights AS
	SELECT d.*,
		CAST(n1 AS FLOAT)/(n1+n2) AS w1,
		CAST(n2 AS FLOAT)/(n1+n2) AS w2
	FROM
		(SELECT DISTINCT(driver_id),
			   COUNT(1) AS n_itineraries,
			   SUM(CASE WHEN distribution_center1 = 1 THEN 1 ELSE 0 END) AS n1,
			   SUM(CASE WHEN distribution_center1 = 2 THEN 1 ELSE 0 END) AS n2
		FROM itineraries
		WHERE driver_id IS NOT NULL
		GROUP BY driver_id) d


/* Calculate driver's agency weights based on the number of itineraries
   done by the driver */
SELECT d.*,
	ROUND(CAST(CAST(n1 AS FLOAT)/(n1+n2) AS NUMERIC), 2) AS w1,
	ROUND(CAST(CAST(n2 AS FLOAT)/(n1+n2) AS NUMERIC), 2) AS w2,
	n1*n2 AS n1xn2
FROM
	(SELECT DISTINCT(driver_id),
		   COUNT(1) AS n_itineraries,
		   SUM(CASE WHEN distribution_center1 = 1 THEN 1 ELSE 0 END) AS n1,
		   SUM(CASE WHEN distribution_center1 = 2 THEN 1 ELSE 0 END) AS n2
	FROM itineraries
	WHERE driver_id IS NOT NULL
	GROUP BY driver_id) d
ORDER BY n1*n2 DESC, n_itineraries DESC


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


/* Build a table with the whole available drivers find in table availables */
CREATE TABLE driver_ag AS
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
	GROUP BY driver_id, distribution_center;


/* Select first and last driver login */
select firstlogin.driver_id, firstlogin.firstlogin, lastlogin.lastlogin, (TO_TIMESTAMP(lastlogin.lastlogin, 'HH24:MI:SS')::TIME) - (TO_TIMESTAMP(firstlogin.firstlogin, 'HH24:MI:SS')::TIME) as workinghours
from firstlogin
inner join lastlogin on  firstlogin.driver_id = lastlogin.driver_id
order by workinghours


/* Pushes per hour of the day */
SELECT EXTRACT(HOUR FROM sent) as hour,
	COUNT(1) as pushes,
	100*CAST(COUNT(1) AS FLOAT)/21525187 as percent
FROM availabilities
GROUP BY EXTRACT(HOUR FROM sent);


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
	
