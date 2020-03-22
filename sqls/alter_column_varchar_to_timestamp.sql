alter table itineraries
alter column created type timestamp using TO_TIMESTAMP(created, 'YY-MM-DD H24:SS')
