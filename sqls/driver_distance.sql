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


DROP TABLE if exists public.driver_day_distance;

CREATE TABLE public.driver_day_distance (
	driver_id varchar NOT NULL,
	"date" timestamp NOT NULL,
	day_distance float8 NULL,
	day_total_sent int4 NULL,
	CONSTRAINT driver_day_distance_pk PRIMARY KEY (driver_id, date)
);
CREATE INDEX driver_day_distance_driver_id_idx ON public.driver_day_distance USING btree (driver_id);


--truncate table driver_day_distance;

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
	push_tolerance INTEGER default 300; -- seconds between pushes to be considered as consecutive;
	push_distance float(8);
	total_distance float(8);
	day_distance float(8);
	day_pushes integer;
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
		day_pushes := 1;
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
			else
			
				-- Insert calculated day data into a new row
				insert into driver_day_distance (driver_id, date, day_distance, day_total_sent )
				values (driver.driver_id, prev_date, day_distance, day_pushes);
			
				--raise notice '';
				--raise notice ' END DAY     - Driver: % --- Date: % --- Day Distance: % --- Day pushes % -----------', driver.driver_id, prev_date, day_distance, day_pushes;
				--raise notice '';
				day_distance := 0;
				day_pushes := 1;
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

	select driver_id, 
		round(cast(sum(day_distance) as decimal), 2) as total_distance, 
		sum(day_total_sent) as total_sent, 
		round(cast(avg(day_distance) as decimal), 2) as avg_day_distance, 
		round(cast(stddev(day_distance) as decimal), 2) as std_day_distance
	from driver_day_distance ddd 
	group by driver_id
          
END $drivers$
LANGUAGE 'plpgsql'

