-- Drop drivers with age null, > 72 and < 18 years old
delete
from driver d 
where age > 72
or age < 18
or age is null 


-- TBD
update driver 
set is_trunk_rented = 'na' -- varchar(1)
where is_trunk_rented is null 


-- Update null values to N/A
update driver
set is_thermal_bag_rented = 'N/A'
where is_thermal_bag_rented is null 


-- TBD
update driver 
set has_thermal_bag = 'na' -- varchar(1)
where has_thermal_bag is null 


-- Update Yes to t
update driver 
set has_loggi_trunk = 't'
where has_loggi_trunk = 'Yes'
-- Assume null as f due to there are only 2 distinct values (Yes and null)
update driver 
set has_loggi_trunk = 'f'
where has_loggi_trunk is null 


-- Update null gender to N/A
update driver 
set gender = 'N/A'
where gender is null 

-- Update null city to São Paulo
update driver 
set city = 'São Paulo'
where city is null 








