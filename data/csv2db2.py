import os, sys
# Add directory where we have our configuration
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + '\\..')) + '\\initial_exploratory_analysis\\')
print(os.path.abspath(__file__ + '..\\'))
# Now we can import our modulue
import practicum_utils as utils

import pandas as pd
import os
import sys

if __name__ != "__main__":
    print('Invalid use')
    exit(0)

show_usage = False
if len(sys.argv) == 1:
    show_usage = True        
elif sys.argv[1] not in ['up', 'drop']:
    print('Invalid usage!')
    show_usage = True

if show_usage:
    print('-'*72)
    print("This file will create tables in postgre db from Loggi's cvs files")
    print('USAGE:')
    print('- Create tables and upload files if tables not exist')
    print('  #> python csv2db2.py up')
    print('- Create tables and upload files dropping tables if they exist')
    print('  #> python csv2db2.py drop')
    print('-'*72)
    exit()


# data directory
dir_data = './supply/'

# files of interest that we will look in directory
files = {
    'availability_dist1_ano.csv': '',
    'availability_dist2_ano.csv': '',
    'itinerary_dist1_ano.csv': '',
    'itinerary_dist2_ano.csv': '',
    'availability_itinerary_dist1_ano.csv': '',
    'availability_itinerary_dist2_ano.csv': '',
    'rejected_dist1_ano.csv': '',
    'rejected_dist2_ano.csv': '',
    'unmatched_dist1_ano.csv': '',
    'unmatched_dist2_ano.csv': '',
    'driver_ano.csv': ''
}

print("Verifing expected files in data directory '{}'... ".format(dir_data), end='')
for f in files.keys(): 
    file = dir_data + f
    assert(os.path.exists(file)==True)
    files[f] = os.path.abspath(file)

print('OK!')
print('Connecting to DB...')
db = utils.global_connect()

# -----------------
# TABLE ITINERARIES
# -----------------

# Check if table already exists
df = utils.run_query("""select t.table_name FROM information_schema.tables as t WHERE t.table_name = 'itineraries'""")
if len(df) == 1:
    print('Table itineraries already exists')
    if len(sys.argv) > 1 and sys.argv[1] == 'drop':
        print('Forced drop...')
        utils.run_query("""DROP TABLE itineraries""", df=False)
    else:
        exit()

print('Creating table itineraries and loading csv files...')

df = utils.run_query("""
CREATE TABLE itineraries
(
    temp                        TEXT,
    itinerary_id                VARCHAR(32) NOT NULL,
    driver_id                   VARCHAR(32),
    created_time                VARCHAR(20),
    accepted_time               VARCHAR(20),
    cancellation_time           VARCHAR(20),
    dropped_time                VARCHAR(20),
    started_time                VARCHAR(20),
    finished_time               VARCHAR(20),
    status                      VARCHAR(30),
    distance                    FLOAT NOT NULL,
    transport_type              VARCHAR(20) NOT NULL,
    product                     VARCHAR(20) NOT NULL,
    product_version             VARCHAR(20) NOT NULL,
    distribution_center         VARCHAR(32) NOT NULL,
    packages                    FLOAT,
    delivered_packages          FLOAT,
    checked_in_time             VARCHAR(20),
    pickup_checkout_time        VARCHAR(20),
    pickup_lat                  FLOAT,
    pickup_lng                  FLOAT,
    waypoints                   INT,
    created_time_datetime       VARCHAR(20),
    finished_time_datetime      VARCHAR(20)
);
COPY itineraries FROM '""" + files['itinerary_dist1_ano.csv'] + """' WITH (format csv, header true, delimiter ',');
COPY itineraries FROM '""" + files['itinerary_dist2_ano.csv'] + """' WITH (format csv, header true, delimiter ',');

ALTER TABLE itineraries DROP COLUMN temp;

SELECT * FROM itineraries LIMIT 5;
""")

if len(df) == 5:
    print('TABLE itineraries created and data was loaded!')

# Looking for duplicates itinerary ids
df = utils.careful_query("""
SELECT itinerary_id, count(1) as dup
FROM itineraries
GROUP BY itinerary_id
HAVING count(1) > 1
""")

# In previous analysis we have found that itineraries presents some duplicated rows
# So we will drop the duplicated ones...
# But if Loggi resend the data again, we should check it again
print('Duplicated Rows: {}'.format(df['dup'].sum() - df.shape[0]))

if len(df) > 0:
    print('Removing duplicates by itinerary_id...')
    df = utils.run_query("""
    -- Remove duplicates
    DELETE FROM itineraries t1
    USING itineraries t2
    WHERE  t1.ctid < t2.ctid                  -- delete the "older" ones
      AND  t1.itinerary_id = t2.itinerary_id; -- list columns that define duplicates

    -- set primary key (only possible with no duplicates)
    ALTER TABLE itineraries ADD PRIMARY KEY (itinerary_id);

    -- Return duplicates (should be 0)
    SELECT itinerary_id, count(1) as dup
    FROM itineraries
    GROUP BY itinerary_id
    HAVING count(1) > 1
    """)

    print('Duplicated Rows: {}'.format(df['dup'].sum() - df.shape[0]))

print('Altering TABLE datetime columns...')
df = utils.run_query("""
ALTER TABLE itineraries ALTER COLUMN created_time TYPE TIMESTAMP USING TO_TIMESTAMP(created_time, 'YY-MM-DD HH24:MI');
ALTER TABLE itineraries ALTER COLUMN accepted_time TYPE TIMESTAMP USING TO_TIMESTAMP(accepted_time, 'YY-MM-DD HH24:MI');
ALTER TABLE itineraries ALTER COLUMN cancellation_time TYPE TIMESTAMP USING TO_TIMESTAMP(cancellation_time, 'YY-MM-DD HH24:MI');
ALTER TABLE itineraries ALTER COLUMN dropped_time TYPE TIMESTAMP USING TO_TIMESTAMP(dropped_time, 'YY-MM-DD HH24:MI');
ALTER TABLE itineraries ALTER COLUMN started_time TYPE TIMESTAMP USING TO_TIMESTAMP(started_time, 'YY-MM-DD HH24:MI');
ALTER TABLE itineraries ALTER COLUMN finished_time TYPE TIMESTAMP USING TO_TIMESTAMP(finished_time, 'YY-MM-DD HH24:MI');
ALTER TABLE itineraries ALTER COLUMN checked_in_time TYPE TIMESTAMP USING TO_TIMESTAMP(checked_in_time, 'YY-MM-DD HH24:MI');
ALTER TABLE itineraries ALTER COLUMN pickup_checkout_time TYPE TIMESTAMP USING TO_TIMESTAMP(pickup_checkout_time, 'YY-MM-DD HH24:MI');
""", df=False)

print('Counting rows in itineraries...')
df = utils.run_query("""SELECT COUNT(1) FROM itineraries""")
print('Total rows found: {}'.format(df.iloc[0,0]))

print('Creating simple indexes for table itineraries...')

create_simple_index_tpl = 'CREATE INDEX {0}_iidx ON itineraries USING btree ({0});'

for idx in ['driver_id', 'created_time', 'accepted_time', 'cancellation_time', 'dropped_time',
            'started_time', 'finished_time', 'checked_in_time', 'pickup_checkout_time',
            'pickup_lat', 'pickup_lng', 'status', 'distance', 'transport_type',
            'distribution_center', 'created_time_datetime', 'finished_time_datetime']:

    print('Creating index "{}_iidx"...'.format(idx))
    r = utils.run_query(create_simple_index_tpl.format(idx), df=False)
