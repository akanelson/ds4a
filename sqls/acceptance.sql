


DROP TABLE if exists public.acceptance;

CREATE TABLE public.acceptance (
	agency_id varchar,
	driver_id varchar,
	itinerary_id varchar,
	offer_time	timestamp,
	availability bool,
	intensity_pushes int,
	distance_to_agency float8,
	driver_position_lat float8,
	driver_position_lng float8,
	previous_work int,
	previous_work_10_days int,
	"label" bool 
);


do $acceptance$
DECLARE

	i_id varchar(32);
	d_id varchar(32);
	a_id varchar(32);
	dc_id varchar(32);
	acc_time timestamp(6);
	availability bool;
	intensity_pushes int;
	distance_to_agency float(8);
	pickup_lat float;
	pickup_lng float;
	driver_lat float;
	driver_lng float;
	distance float;
	previous_work int;
	previous_work_10_days int;
	label bool;
	
	rej_time timestamp;
	aux int;
	dc_contador int;
	dist_cent varchar(32);
	contador int;
	
	cur_itinerary CURSOR for
   	SELECT * FROM itinerary i where distribution_center = dist_cent; --limit 15; 
   
   
    cur_rejected CURSOR for
  	select * from rejected r where itinerary_id = i_id order by sent;

begin

	-- agency A: 58cfe3b975dd7cbd1ac84d555640bfd9
	-- agency B: 6e7dacf2149d053183fe901e3cfd8b82
	
	dist_cent := '58cfe3b975dd7cbd1ac84d555640bfd9';
	contador := 1;

	select count(*)
	into dc_contador
	from itinerary i
	where distribution_center = dist_cent;	
	
	FOR itinerary IN cur_itinerary LOOP
		i_id := itinerary.itinerary_id;	
		d_id := itinerary.driver_id;
		a_id := itinerary.distribution_center;
		acc_time := itinerary.accepted_time;
		pickup_lat := itinerary.pickup_lat;
		pickup_lng := itinerary.pickup_lng;
		
		-- label
		label := true;
	
	
		-- intensity pushes
		select count(*)
		into intensity_pushes
		from availability a 
		where driver_id = d_id
		and distribution_center = a_id
		and sent_f between (acc_time - interval '1 hour') and acc_time; 	
	
	
		-- availability	
		availability := true;
		if intensity_pushes > 0 then
			select count(*)
			into aux 
			from itinerary i
			where driver_id = d_id
			and accepted_time < acc_time
			and finished_time > acc_time;

			if aux > 0 then
				availability := false;
			end if;
		else 
			availability := false;
		end if;
		
		-- distance_to_agency
		select lat, lng
		into driver_lat, driver_lng
		from availability a 
		where driver_id = d_id
		and distribution_center = a_id
		and sent_f between (acc_time - interval '1 hour') and acc_time 	
		order by sent_f desc   
		limit 1;
		
		if driver_lat is not null and driver_lng is not null then
			distance := calculate_distance(pickup_lat, pickup_lng, driver_lat, driver_lng, 'K');
		else
			distance := -1;
		end if;
		
		-- previous work
		select count(*)
		into previous_work
		from itinerary i 
		where driver_id = d_id
		and distribution_center = a_id
		and accepted_time < acc_time;

		-- previous work 10 days
		select count(*)
		into previous_work_10_days
		from itinerary i 
		where driver_id = d_id
		and distribution_center = a_id
		and accepted_time > (acc_time - interval '10 days')
		and accepted_time < acc_time;
	
		raise notice '';
		raise notice '';
		raise notice '%/% | D. Center % | Driver % | Itinerary % | Offer Time % | Availability % | Intensity % | Distance % | Driver Lat % | Driver Lng % | Previous W % | Previous W 10 D % | Label %',
		contador, dc_contador, a_id, d_id, i_id, acc_time, availability, intensity_pushes,distance, driver_lat, driver_lng, previous_work, previous_work_10_days, label;
		contador := contador + 1;
		
		insert into acceptance (agency_id, driver_id, itinerary_id,	offer_time, availability, intensity_pushes, distance_to_agency, driver_position_lat, driver_position_lng, previous_work, previous_work_10_days, label)
		values (a_id, d_id, i_id, acc_time, availability, intensity_pushes,distance, driver_lat, driver_lng, previous_work, previous_work_10_days, label);
	
	
		FOR rejected IN cur_rejected loop
						
			d_id := rejected.driver_id;
			rej_time := rejected.sent;			
	
			-- label
			label := false;
	
			-- intensity pushes
			select count(*)
			into intensity_pushes
			from availability a 
			where driver_id = d_id
			and distribution_center = a_id
			and sent_f between (rej_time - interval '1 hour') and rej_time; 
		
			
			-- availability	
			availability := true;
			if intensity_pushes > 0 then
				select count(*)
				into aux 
				from itinerary i
				where driver_id = d_id
				and accepted_time < rej_time
				and finished_time > rej_time;
	
				if aux > 0 then
					availability := false;
				end if;
			else 
				availability := false;
			end if;
		
			-- distance_to_agency
			select lat, lng
			into driver_lat, driver_lng
			from availability a 
			where driver_id = d_id
			and distribution_center = a_id
			and sent_f between (rej_time - interval '1 hour') and rej_time 	
			order by sent_f desc   
			limit 1;
		
			if driver_lat is not null and driver_lng is not null then
				distance := calculate_distance(pickup_lat, pickup_lng, driver_lat, driver_lng, 'K');
			else
				distance := -1;
			end if;	
		
			-- previous work
			select count(*)
			into previous_work
			from itinerary i 
			where driver_id = d_id 
			and distribution_center = a_id
			and accepted_time < rej_time;
	
			-- previous work 10 days
			select count(*)
			into previous_work_10_days
			from itinerary i 
			where driver_id = d_id
			and distribution_center = a_id 
			and accepted_time > (rej_time - interval '10 days')
			and accepted_time < rej_time;		

			raise notice '        D. Center % | Driver % | Itinerary % | Offer Time % | Availability % | Intensity % | Distance % | Driver Lat % | Driver Lng % | Previous W % | Previous W 10 D % | Label %',
			a_id, d_id, i_id, rej_time, availability, intensity_pushes, distance, driver_lat, driver_lng, previous_work, previous_work_10_days, label;

			insert into acceptance (agency_id, driver_id, itinerary_id,	offer_time, availability, intensity_pushes, distance_to_agency, driver_position_lat, driver_position_lng, previous_work, previous_work_10_days, label)
			values (a_id, d_id, i_id, rej_time, availability, intensity_pushes,distance, driver_lat, driver_lng, previous_work, previous_work_10_days, label);
		
    	end loop;
    	
	end loop;

	raise notice '';
	raise notice '';	
	raise notice '========== END PROCESS =============';
          
END $acceptance$
LANGUAGE 'plpgsql'






	
	

