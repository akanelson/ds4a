-- Build new av2it table

create table av2it_oozma as
select i.distribution_center , i.itinerary_id , i.driver_id , a.lat , a.lng , a.sent_f , 'deliverying' as sent_type 
from itinerary i 
inner join availability a on i.driver_id = a.driver_id 
where a.sent_f between i.started_time and i.finished_time;


insert into av2it_oozma (distribution_center , itinerary_id , driver_id , lat , lng, sent_f , sent_type )
select i.distribution_center , i.itinerary_id , i.driver_id , a.lat , a.lng , a.sent_f , 'picking up'
from itinerary i 
inner join availability a on i.driver_id = a.driver_id 
where a.sent_f between i.accepted_time and i.checked_in_time; 

