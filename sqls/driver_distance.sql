/*
 * Build a new driver_day_distance table
 * and calculates the distance driven by each driver each day
 * and saves a new row for each driver/date driven.
 * 
 * For the calculation, it checks the time between each push and keeps times under
 * the push_tolarence definition and discard times above the tolerance.
 * 
 * For the distance, it takes the previous and current latitude and longitude and compute
 * the line distance in between.
 * 
 * Once the table is built, a final query is run with the averages and standard deviation
 * for drivers globally.
 * */


CREATE OR REPLACE FUNCTION public.calculate_distance(lat1 double precision, lon1 double precision, lat2 double precision, lon2 double precision, units character varying)
 RETURNS double precision
 LANGUAGE plpgsql
AS $function$
    DECLARE
        dist float = 0;
        radlat1 float;
        radlat2 float;
        theta float;
        radtheta float;
    BEGIN
        IF lat1 = lat2 OR lon1 = lon2
            THEN RETURN dist;
        ELSE
            radlat1 = pi() * lat1 / 180;
            radlat2 = pi() * lat2 / 180;
            theta = lon1 - lon2;
            radtheta = pi() * theta / 180;
            dist = sin(radlat1) * sin(radlat2) + cos(radlat1) * cos(radlat2) * cos(radtheta);

            IF dist > 1 THEN dist = 1; END IF;

            dist = acos(dist);
            dist = dist * 180 / pi();
            dist = dist * 60 * 1.1515;

            IF units = 'K' THEN dist = dist * 1.609344; END IF;
            IF units = 'N' THEN dist = dist * 0.8684; END IF;

            RETURN dist;
        END IF;
    END;
$function$
;


DROP TABLE if exists public.driver_day_distance;

CREATE TABLE public.driver_day_distance (
	driver_id varchar NOT NULL,
	"date" timestamp NOT NULL,
	day_distance float8 NULL,
	day_total_sent int4 NULL,
	day_distance_with_it float8 NULL,
	day_total_sent_with_it int4 NULL,
	CONSTRAINT driver_day_distance_pk PRIMARY KEY (driver_id, date)
);

--CREATE INDEX driver_day_distance_driver_id_idx ON public.driver_day_distance USING btree (driver_id);

do $drivers$
DECLARE
    
	d_id varchar(32);
	curr_push timestamp(6);
	curr_lat float(8);
	curr_lng float(8);
	curr_date date;
	prev_push timestamp(6);
	prev_lat float(8);
	prev_lng float(8);
	prev_date date;
	diff_push FLOAT(10);
	push_tolerance INTEGER default 600; -- seconds between pushes to be considered as consecutive;
	push_distance float(8);
	total_distance float(8);
	day_distance float(8);
	day_distance_it float(8);
	day_pushes integer;
	day_pushes_it integer;
	total_drivers integer;
	drivers_count integer;


	cur_drivers CURSOR for
   	SELECT distinct(driver_id) FROM availabilities; 
  	
    cur_pushes CURSOR for
  	select * from availabilities where driver_id = d_id order by sent;

begin
	
	raise notice ' - Calculating total unique drivers .... -';	
	--select into total_drivers count(distinct(driver_id)) from availabilities;
	total_drivers := 8195;
	drivers_count := 0;
	
	FOR driver IN cur_drivers LOOP
		d_id := driver.driver_id;
		prev_push := null;
		prev_date := null;
		total_distance := 0;
		day_distance := 0;
		day_pushes := 0;
		day_distance_it := 0;
		day_pushes_it := 0;
		drivers_count := drivers_count + 1;
	    
		--raise notice '';
		--raise notice '';
		raise notice '% / % --- NEW Driver: %', drivers_count, total_drivers, driver.driver_id;	
	
	
		FOR push IN cur_pushes loop

	    	curr_push := push.sent;
	    	curr_date := date(push.sent);
	    	curr_lat := push.lat;
	    	curr_lng := push.lng;

	    	if prev_push is null then
	    		prev_push := curr_push;
	    		prev_date := curr_date;
	    		prev_lat := curr_lat;
	    		prev_lng := curr_lng;
	    	end if;
	    
	    	diff_push := extract(EPOCH from curr_push) - extract(EPOCH from prev_push);
			if abs(diff_push) <= push_tolerance then
				push_distance := calculate_distance(prev_lat, prev_lng, curr_lat, curr_lng, 'K');
			else
				push_distance := 0;
			end if;
			
			--raise notice '    # % Prev: % - Curr % - Diff % - Distance % - Day Distance % - Total Distance % - PrevPos % - CurrPos % ', day_pushes, prev_push, curr_push, diff_push, push_distance, day_distance, total_distance, cast(prev_lat as varchar)||','||cast(prev_lng as varchar), cast(curr_lat as varchar)||','||cast(curr_lng as varchar);
		
			if curr_date = prev_date then
				day_distance := day_distance + push_distance;
				day_pushes := day_pushes + 1;
				
				if push.itinerary_id is not null then
					--raise notice ' IT ASSIGNED   # % - Day Distance % - With ITINERARY %', day_pushes_it, day_distance, day_distance_it;
					day_distance_it := day_distance_it + push_distance;
					day_pushes_it := day_pushes_it + 1;
				end if;
			
			else
			
				-- Insert calculated day data into a new row
				insert into driver_day_distance (driver_id, date, day_distance, day_total_sent, day_distance_with_it, day_total_sent_with_it)
				values (driver.driver_id, prev_date, day_distance, day_pushes, day_distance_it, day_pushes_it);
			
				--raise notice '';
				--raise notice ' END DAY     - Driver: % --- Date: % --- Day Distance: % --- Day pushes % -----------', driver.driver_id, prev_date, day_distance, day_pushes;
				--raise notice '';
				day_distance := 0;
				day_pushes := 0;
				day_distance_it := 0;
				day_pushes_it := 0;				
			end if;
		
			total_distance := total_distance + push_distance;
		
			prev_push := curr_push;
			prev_date := curr_date;
			prev_lat := curr_lat;
	    	prev_lng := curr_lng;
    	end loop;
    	
		--raise notice '';
    	--raise notice '========== END Driver: % - Total distance: %', driver.driver_id, total_distance;

	end loop;

	raise notice '';
	raise notice '';	
	raise notice '========== END PROCESS =============';
          
END $drivers$
LANGUAGE 'plpgsql'


/*
 * After the script above runs, run the following query
 * to get a consolidated values per Driver.
 * 

select driver_id, 
	round(cast(sum(day_distance) as decimal), 2) as total_distance, 
	sum(day_total_sent) as total_sent, 
	round(cast(avg(day_distance) as decimal), 2) as avg_day_distance, 
	round(cast(stddev(day_distance) as decimal), 2) as std_day_distance,
	round(cast(sum(day_distance_with_it) as decimal), 2) as total_distance_with_it, 
	sum(day_total_sent_with_it) as total_sent_with_it, 
	round(cast(avg(day_distance_with_it) as decimal), 2) as avg_day_distance_with_it, 
	round(cast(stddev(day_distance_with_it) as decimal), 2) as std_day_distance_with_it
from driver_day_distance ddd 
group by driver_id;

*/





