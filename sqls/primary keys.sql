DROP INDEX public.id_aidx;
ALTER TABLE public.availability ADD CONSTRAINT availability_pk PRIMARY KEY (id);


-- Remove duplicated drivers
delete 
from driver d2 
where driver_id in (
	select driver_id 
	from driver d 
	group by driver_id 
	having count(*) > 1
	)
and vehicle_status = 'Waiting review'

-- Remove duplicated drivers
delete 
from driver d2 
where driver_id in (
	select driver_id 
	from driver d 
	group by driver_id 
	having count(*) > 1
	)
and vehicle_status = 'Invalid'
DROP INDEX public.driver_id_aidx5;
ALTER TABLE public.driver ADD CONSTRAINT driver_pk PRIMARY KEY (driver_id);



DROP INDEX public.sent_aidx3;
DROP INDEX public.itinerary_id_aidx3;
DROP INDEX public.driver_id_aidx3;
ALTER TABLE public.rejected ADD CONSTRAINT rejected_pk PRIMARY KEY (distribution_center, itinerary_id,driver_id,sent);


ALTER TABLE public.unmatched ADD CONSTRAINT unmatched_pk PRIMARY KEY (distribution_center,itinerary_id,driver_id,sent);
DROP INDEX public.driver_id_aidx2;
DROP INDEX public.itinerary_id_aidx2;
DROP INDEX public.sent_aidx2;


ALTER TABLE public.av2it_oozma ADD CONSTRAINT av2it_oozma_pk PRIMARY KEY (distribution_center,itinerary_id,driver_id,sent_f);
