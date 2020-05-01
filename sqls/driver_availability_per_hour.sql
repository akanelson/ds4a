
select driver_id, extract(year from sent_f)||'-'||lpad(cast(extract(month from sent_f) as varchar),2,'0')||'-'||lpad(cast(extract(day from sent_f) as varchar),2,'0') as date, extract(dow from sent_f) as dow,
	count(case when extract(hour from sent_f) = 0 then 1 end) as h0,
	count(case when extract(hour from sent_f) = 1 then 1 end) as h1,
	count(case when extract(hour from sent_f) = 2 then 1 end) as h2,
	count(case when extract(hour from sent_f) = 3 then 1 end) as h3,
	count(case when extract(hour from sent_f) = 4 then 1 end) as h4,
	count(case when extract(hour from sent_f) = 5 then 1 end) as h5,
	count(case when extract(hour from sent_f) = 6 then 1 end) as h6,
	count(case when extract(hour from sent_f) = 7 then 1 end) as h7,
	count(case when extract(hour from sent_f) = 8 then 1 end) as h8,
	count(case when extract(hour from sent_f) = 9 then 1 end) as h9,
	count(case when extract(hour from sent_f) = 10 then 1 end) as h10,
	count(case when extract(hour from sent_f) = 11 then 1 end) as h11,
	count(case when extract(hour from sent_f) = 12 then 1 end) as h12,
	count(case when extract(hour from sent_f) = 13 then 1 end) as h13,
	count(case when extract(hour from sent_f) = 14 then 1 end) as h14,
	count(case when extract(hour from sent_f) = 15 then 1 end) as h15,
	count(case when extract(hour from sent_f) = 16 then 1 end) as h16,
	count(case when extract(hour from sent_f) = 17 then 1 end) as h17,
	count(case when extract(hour from sent_f) = 18 then 1 end) as h18,
	count(case when extract(hour from sent_f) = 19 then 1 end) as h19,
	count(case when extract(hour from sent_f) = 20 then 1 end) as h20,
	count(case when extract(hour from sent_f) = 21 then 1 end) as h21,
	count(case when extract(hour from sent_f) = 22 then 1 end) as h22,
	count(case when extract(hour from sent_f) = 23 then 1 end) as h23
into table driver_availability_per_hour
from availability a
group by driver_id, extract(year from sent_f)||'-'||lpad(cast(extract(month from sent_f) as varchar),2,'0')||'-'||lpad(cast(extract(day from sent_f) as varchar),2,'0'), extract(dow from sent_f)
order by driver_id, date, dow 



