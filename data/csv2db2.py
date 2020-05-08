import os, sys
from shutil import which
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

# ---------------
# TABLE ITINERARY
# ---------------

# Check if table already exists
df = utils.run_query("""select t.table_name FROM information_schema.tables as t WHERE t.table_name = 'itinerary'""")
if len(df) == 1:
    print('Table itinerary already exists')
    if len(sys.argv) > 1 and sys.argv[1] == 'drop':
        print('Forced drop...')
        utils.run_query("""DROP TABLE itinerary""", df=False)
    else:
        exit()

print('Creating table itinerary and loading csv files...')

df = utils.run_query("""
CREATE TABLE itinerary
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
COPY itinerary FROM '""" + files['itinerary_dist1_ano.csv'] + """' WITH (format csv, header true, delimiter ',');
COPY itinerary FROM '""" + files['itinerary_dist2_ano.csv'] + """' WITH (format csv, header true, delimiter ',');

ALTER TABLE itinerary DROP COLUMN temp;

SELECT * FROM itinerary LIMIT 5;
""")

if len(df) == 5:
    print('TABLE itinerary created and data was loaded!')

# Looking for duplicates itinerary ids
df = utils.careful_query("""
SELECT itinerary_id, count(1) as dup
FROM itinerary
GROUP BY itinerary_id
HAVING count(1) > 1
""")

# In previous analysis we have found that itinerary presents some duplicated rows
# So we will drop the duplicated ones...
# But if Loggi resend the data again, we should check it again
print('Duplicated Rows: {}'.format(df['dup'].sum() - df.shape[0]))

if len(df) > 0:
    print('Removing duplicates by itinerary_id...')
    df = utils.run_query("""
    -- Remove duplicates
    DELETE FROM itinerary t1
    USING itinerary t2
    WHERE  t1.ctid < t2.ctid                  -- delete the "older" ones
      AND  t1.itinerary_id = t2.itinerary_id; -- list columns that define duplicates

    -- set primary key (only possible with no duplicates)
    ALTER TABLE itinerary ADD PRIMARY KEY (itinerary_id);

    -- Return duplicates (should be 0)
    SELECT itinerary_id, count(1) as dup
    FROM itinerary
    GROUP BY itinerary_id
    HAVING count(1) > 1
    """)

    print('Duplicated Rows: {}'.format(df['dup'].sum() - df.shape[0]))

print('Altering TABLE datetime columns...')
df = utils.run_query("""
ALTER TABLE itinerary ALTER COLUMN created_time TYPE TIMESTAMP USING TO_TIMESTAMP(created_time, 'YY-MM-DD HH24:MI:SS');
ALTER TABLE itinerary ALTER COLUMN accepted_time TYPE TIMESTAMP USING TO_TIMESTAMP(accepted_time, 'YY-MM-DD HH24:MI:SS');
ALTER TABLE itinerary ALTER COLUMN cancellation_time TYPE TIMESTAMP USING TO_TIMESTAMP(cancellation_time, 'YY-MM-DD HH24:MI:SS');
ALTER TABLE itinerary ALTER COLUMN dropped_time TYPE TIMESTAMP USING TO_TIMESTAMP(dropped_time, 'YY-MM-DD HH24:MI:SS');
ALTER TABLE itinerary ALTER COLUMN started_time TYPE TIMESTAMP USING TO_TIMESTAMP(started_time, 'YY-MM-DD HH24:MI:SS');
ALTER TABLE itinerary ALTER COLUMN finished_time TYPE TIMESTAMP USING TO_TIMESTAMP(finished_time, 'YY-MM-DD HH24:MI:SS');
ALTER TABLE itinerary ALTER COLUMN checked_in_time TYPE TIMESTAMP USING TO_TIMESTAMP(checked_in_time, 'YY-MM-DD HH24:MI:SS');
ALTER TABLE itinerary ALTER COLUMN pickup_checkout_time TYPE TIMESTAMP USING TO_TIMESTAMP(pickup_checkout_time, 'YY-MM-DD HH24:MI:SS');
""", df=False)

print('Counting rows in itinerary...')
df = utils.run_query("""SELECT COUNT(1) FROM itinerary""")
print('Total rows found: {}'.format(df.iloc[0,0]))

print('Creating simple indexes for table itinerary...')

create_simple_index_tpl = 'CREATE INDEX {0}_iidx ON itinerary USING btree ({0});'

for idx in ['driver_id', 'created_time', 'accepted_time', 'cancellation_time', 'dropped_time',
            'started_time', 'finished_time', 'checked_in_time', 'pickup_checkout_time',
            'pickup_lat', 'pickup_lng', 'status', 'distance', 'transport_type',
            'distribution_center', 'created_time_datetime', 'finished_time_datetime']:

    print('Creating index "{}_iidx"...'.format(idx))
    r = utils.run_query(create_simple_index_tpl.format(idx), df=False)

# Agency 1: 6e7dacf2149d053183fe901e3cfd8b82
# Agency 2: 58cfe3b975dd7cbd1ac84d555640bfd9

# --------------
# availability
# --------------

# Check if table already exists
df = utils.run_query("""select t.table_name FROM information_schema.tables as t WHERE t.table_name = 'availability'""")
if len(df) == 1:
    print('Table availability already exists')
    if len(sys.argv) > 1 and sys.argv[1] == 'drop':
        print('Forced drop...')
        utils.run_query("""DROP TABLE availability""", df=False)
    else:
        exit()


tpl = ["SELECT '{}' as distribution_center, * INTO availability FROM tmp_availability",
       "INSERT INTO availability SELECT '{}' as distribution_center, * FROM tmp_availability"]

for fn, agency, _tpl in [
    ('availability_dist1_ano.csv', '6e7dacf2149d053183fe901e3cfd8b82', tpl[0]),
    ('availability_dist2_ano.csv', '58cfe3b975dd7cbd1ac84d555640bfd9', tpl[1])]:

    print('Creating temporal table for availabilies.\nLoading csv file {}.\nThis will take some time...'.format(fn))

    create_table_from_csv = """
        CREATE TEMPORARY TABLE tmp_availability
        (
            temp            INT,
            id              VARCHAR(32) NOT NULL,
            driver_id       VARCHAR(32) NOT NULL,
            lng             FLOAT,
            lat             FLOAT,
            sent_f          VARCHAR(20)
        );

        /* Copy command */
        {0};

        ALTER TABLE tmp_availability DROP COLUMN temp;
        ALTER TABLE tmp_availability ALTER COLUMN sent_f TYPE TIMESTAMP USING TO_TIMESTAMP(sent_f, 'YY-MM-DD HH24:MI:SS');

        /* first time select into availability, second time insert into availability*/
        {1};

        DROP TABLE tmp_availability;

        SELECT * from availability limit 5;
    """

    copy_cmd = """COPY tmp_availability FROM '{0}' WITH (format csv, header true, delimiter ',');""".format(files[fn])
    # if exists compressed version of file    
    if sys.platform == 'win32' and os.path.exists(files[fn] + '.gz'):
        # path to 7zip
        seven_zip = which('7z')
        if seven_zip == None:
            print('WARNING: can not locate program 7z to copy compressed file into DB')
            print('- In Windows, Postgre can not handle big plain CSV files!')
            print('- It is probabily that this uploading ends in an exception.')
        else:
            copy_cmd = """COPY tmp_availability FROM PROGRAM '"{0}" e -so "{1}"' DELIMITER ',' CSV HEADER;""".format(seven_zip, files[fn] + '.gz')

    df = utils.run_query(create_table_from_csv.format(copy_cmd, _tpl.format(agency)), df=False)

    df = utils.run_query("""select * from availability limit 5;""")
    if len(df) == 5:
        print('File {} loaded!'.format(fn))

print('Counting rows in availability...')
df = utils.run_query("""SELECT COUNT(1) FROM availability""")
print('Total rows found: {}'.format(df.iloc[0,0]))

print('Creating simple indexes for table availability (slow process)...')

create_simple_index_tpl = 'CREATE INDEX {0}_aidx ON availability USING btree ({0});'

for idx in ['id', 'distribution_center', 'driver_id', 'sent_f']:
    print('Creating index "{}_aidx"...'.format(idx))
    r = utils.run_query(create_simple_index_tpl.format(idx), df=False)


# ---------
# UNMATCHED
# ---------

# Check if table already exists
df = utils.run_query("""select t.table_name FROM information_schema.tables as t WHERE t.table_name = 'unmatched'""")
if len(df) == 1:
    print('Table unmatched already exists')
    if len(sys.argv) > 1 and sys.argv[1] == 'drop':
        print('Forced drop...')
        utils.run_query("""DROP TABLE unmatched""", df=False)
    else:
        exit()


tpl = ["SELECT '{}' as distribution_center, * INTO unmatched FROM tmp_unmatched",
       "INSERT INTO unmatched SELECT '{}' as distribution_center, * FROM tmp_unmatched"]

for fn, agency, _tpl in [
    ('unmatched_dist1_ano.csv', '6e7dacf2149d053183fe901e3cfd8b82', tpl[0]),
    ('unmatched_dist2_ano.csv', '58cfe3b975dd7cbd1ac84d555640bfd9', tpl[1])]:

    print('Creating temporal table for unmatched.\nLoading csv file {}.\nThis will take some time...'.format(fn))

    create_table_from_csv = """
        CREATE TEMPORARY TABLE tmp_unmatched (
            temp            INT,
            itinerary_id    VARCHAR(32) NOT NULL,
            driver_id       VARCHAR(32) NOT NULL,
            sent            VARCHAR(26)
        );

        /* Copy command */
        {0};

        ALTER TABLE tmp_unmatched DROP COLUMN temp;
        ALTER TABLE tmp_unmatched ALTER COLUMN sent TYPE TIMESTAMP USING TO_TIMESTAMP(sent, 'YY-MM-DD HH24:MI:SS');

        /* first time select into unmatched, second time insert into unmatched */
        {1};

        DROP TABLE tmp_unmatched;

        SELECT * from unmatched limit 5;
    """

    copy_cmd = """COPY tmp_unmatched FROM '{0}' WITH (format csv, header true, delimiter ',');""".format(files[fn])
    # if exists compressed version of file    
    if sys.platform == 'win32' and os.path.exists(files[fn] + '.gz'):
        # path to 7zip
        seven_zip = which('7z')
        if seven_zip == None:
            print('WARNING: can not locate program 7z to copy compressed file into DB')
            print('- In Windows, Postgre can not handle big plain CSV files!')
            print('- It is probabily that this uploading ends in an exception.')
        else:
            copy_cmd = """COPY tmp_unmatched FROM PROGRAM '"{0}" e -so "{1}"' DELIMITER ',' CSV HEADER;""".format(seven_zip, files[fn] + '.gz')

    df = utils.run_query(create_table_from_csv.format(copy_cmd, _tpl.format(agency)), df=False)

    df = utils.run_query("""select * from unmatched limit 5;""")
    if len(df) == 5:
        print('File {} loaded!'.format(fn))

print('Counting rows in unmatched...')
df = utils.run_query("""SELECT COUNT(1) FROM unmatched""")
print('Total rows found: {}'.format(df.iloc[0,0]))

print('Creating simple indexes for table unmatched (slow process)...')

create_simple_index_tpl = 'CREATE INDEX {0}_aidx2 ON unmatched USING btree ({0});'

for idx in ['itinerary_id', 'driver_id', 'sent']:
    print('Creating index "{}_aidx2"...'.format(idx))
    r = utils.run_query(create_simple_index_tpl.format(idx), df=False)


# --------
# REJECTED
# --------

# Check if table already exists
df = utils.run_query("""select t.table_name FROM information_schema.tables as t WHERE t.table_name = 'rejected'""")
if len(df) == 1:
    print('Table rejected already exists')
    if len(sys.argv) > 1 and sys.argv[1] == 'drop':
        print('Forced drop...')
        utils.run_query("""DROP TABLE rejected""", df=False)
    else:
        exit()


tpl = ["SELECT '{}' as distribution_center, * INTO rejected FROM tmp_rejected",
       "INSERT INTO rejected SELECT '{}' as distribution_center, * FROM tmp_rejected"]

for fn, agency, _tpl in [
    ('rejected_dist1_ano.csv', '6e7dacf2149d053183fe901e3cfd8b82', tpl[0]),
    ('rejected_dist2_ano.csv', '58cfe3b975dd7cbd1ac84d555640bfd9', tpl[1])]:

    print('Creating temporal table for rejected.\nLoading csv file {}.\nThis will take some time...'.format(fn))

    create_table_from_csv = """
        CREATE TEMPORARY TABLE tmp_rejected (
            temp            INT,
            itinerary_id    VARCHAR(32) NOT NULL,
            driver_id       VARCHAR(32) NOT NULL,
            sent            VARCHAR(26)
        );

        /* Copy command */
        {0};

        ALTER TABLE tmp_rejected DROP COLUMN temp;
        ALTER TABLE tmp_rejected ALTER COLUMN sent TYPE TIMESTAMP USING TO_TIMESTAMP(sent, 'YY-MM-DD HH24:MI:SS');

        /* first time select into rejected, second time insert into rejected */
        {1};

        DROP TABLE tmp_rejected;

        SELECT * from rejected limit 5;
    """

    copy_cmd = """COPY tmp_rejected FROM '{0}' WITH (format csv, header true, delimiter ',');""".format(files[fn])
    # if exists compressed version of file    
    if sys.platform == 'win32' and os.path.exists(files[fn] + '.gz'):
        # path to 7zip
        seven_zip = which('7z')
        if seven_zip == None:
            print('WARNING: can not locate program 7z to copy compressed file into DB')
            print('- In Windows, Postgre can not handle big plain CSV files!')
            print('- It is probabily that this uploading ends in an exception.')
        else:
            copy_cmd = """COPY tmp_rejected FROM PROGRAM '"{0}" e -so "{1}"' DELIMITER ',' CSV HEADER;""".format(seven_zip, files[fn] + '.gz')

    df = utils.run_query(create_table_from_csv.format(copy_cmd, _tpl.format(agency)), df=False)

    df = utils.run_query("""select * from rejected limit 5;""")
    if len(df) == 5:
        print('File {} loaded!'.format(fn))

print('Counting rows in rejected...')
df = utils.run_query("""SELECT COUNT(1) FROM rejected""")
print('Total rows found: {}'.format(df.iloc[0,0]))

print('Creating simple indexes for table rejected (slow process)...')

create_simple_index_tpl = 'CREATE INDEX {0}_aidx3 ON rejected USING btree ({0});'

for idx in ['itinerary_id', 'driver_id', 'sent']:
    print('Creating index "{}_aidx3"...'.format(idx))
    r = utils.run_query(create_simple_index_tpl.format(idx), df=False)


# ----------------------------
# Availabilities 2 Itineraries
# ----------------------------

# Check if table already exists
df = utils.run_query("""select t.table_name FROM information_schema.tables as t WHERE t.table_name = 'av2it'""")
if len(df) == 1:
    print('Table av2it already exists')
    if len(sys.argv) > 1 and sys.argv[1] == 'drop':
        print('Forced drop...')
        utils.run_query("""DROP TABLE av2it""", df=False)
    else:
        exit()


tpl = ["SELECT '{}' as distribution_center, * INTO av2it FROM tmp_av2it",
       "INSERT INTO av2it SELECT '{}' as distribution_center, * FROM tmp_av2it"]

for fn, agency, _tpl in [
    ('availability_itinerary_dist1_ano.csv', '6e7dacf2149d053183fe901e3cfd8b82', tpl[0]),
    ('availability_itinerary_dist2_ano.csv', '58cfe3b975dd7cbd1ac84d555640bfd9', tpl[1])]:

    print('Creating temporal table for av2it.\nLoading csv file {}.\nThis will take some time...'.format(fn))

    create_table_from_csv = """
        CREATE TEMPORARY TABLE tmp_av2it (
            temp            INT,
            availability_id VARCHAR(32) NOT NULL,
            itinerary_id    VARCHAR(32) NOT NULL
        );

        /* Copy command */
        {0};

        ALTER TABLE tmp_av2it DROP COLUMN temp;

        /* first time select into av2it, second time insert into av2it */
        {1};

        DROP TABLE tmp_av2it;

        SELECT * from av2it limit 5;
    """

    copy_cmd = """COPY tmp_av2it FROM '{0}' WITH (format csv, header true, delimiter ',');""".format(files[fn])
    # if exists compressed version of file    
    if sys.platform == 'win32' and os.path.exists(files[fn] + '.gz'):
        # path to 7zip
        seven_zip = which('7z')
        if seven_zip == None:
            print('WARNING: can not locate program 7z to copy compressed file into DB')
            print('- In Windows, Postgre can not handle big plain CSV files!')
            print('- It is probabily that this uploading ends in an exception.')
        else:
            copy_cmd = """COPY tmp_av2it FROM PROGRAM '"{0}" e -so "{1}"' DELIMITER ',' CSV HEADER;""".format(seven_zip, files[fn] + '.gz')

    df = utils.run_query(create_table_from_csv.format(copy_cmd, _tpl.format(agency)), df=False)

    df = utils.run_query("""select * from av2it limit 5;""")
    if len(df) == 5:
        print('File {} loaded!'.format(fn))

print('Counting rows in av2it...')
df = utils.run_query("""SELECT COUNT(1) FROM av2it""")
print('Total rows found: {}'.format(df.iloc[0,0]))

print('Creating simple indexes for table av2it (slow process)...')

create_simple_index_tpl = 'CREATE INDEX {0}_aidx4 ON av2it USING btree ({0});'

for idx in ['itinerary_id', 'availability_id']:
    print('Creating index "{}_aidx4"...'.format(idx))
    r = utils.run_query(create_simple_index_tpl.format(idx), df=False)

# ------
# DRIVER
# ------

# Check if table already exists
df = utils.run_query("""select t.table_name FROM information_schema.tables as t WHERE t.table_name = 'driver'""")
if len(df) == 1:
    print('Table driver already exists')
    if len(sys.argv) > 1 and sys.argv[1] == 'drop':
        print('Forced drop...')
        utils.run_query("""DROP TABLE driver""", df=False)
    else:
        exit()


for fn in ['driver_ano.csv']:

    print('Creating temporal table for drivers.\nLoading csv file {}.\nThis will take some time...'.format(fn))

    create_table_from_csv = """
        CREATE TEMPORARY TABLE tmp_driver (
            temp                        INT,
            driver_id                   VARCHAR(32) NOT NULL,
            created                     VARCHAR(26),
            onboard_date                VARCHAR(26),
            activation_date             VARCHAR(26),
            marital_status              VARCHAR(10),
            is_trunk_rented             VARCHAR(1),
            is_thermal_bag_rented       VARCHAR(10),
            has_thermal_bag             VARCHAR(1),
            has_loggi_trunk             VARCHAR(3),
            gender                      VARCHAR(10),
            transport_type              VARCHAR(10),
            city                        VARCHAR(20),
            operational_status          VARCHAR(20),
            trunk_capacity              FLOAT,
            rescinded_date              VARCHAR(26),
            email_is_verified           VARCHAR(1),
            age                         FLOAT,
            vehicle_license_plate_type  VARCHAR(10),
            cnh_status                  VARCHAR(20),
            vehicle_status              VARCHAR(20),
            has_all_documents_valid     VARCHAR(1),
            first_itinerary_id          VARCHAR(32),
            first_itinerary_created     VARCHAR(26),
            attend_corp                 VARCHAR(1),
            attend_presto               VARCHAR(1),
            attend_pro                  VARCHAR(1)
        );

        /* Copy command */
        {0};

        ALTER TABLE tmp_driver DROP COLUMN temp;
        ALTER TABLE tmp_driver ALTER COLUMN created TYPE TIMESTAMP USING TO_TIMESTAMP(created, 'YY-MM-DD HH24:MI:SS');
        ALTER TABLE tmp_driver ALTER COLUMN onboard_date TYPE TIMESTAMP USING TO_TIMESTAMP(onboard_date, 'YY-MM-DD HH24:MI:SS');
        ALTER TABLE tmp_driver ALTER COLUMN activation_date TYPE TIMESTAMP USING TO_TIMESTAMP(activation_date, 'YY-MM-DD HH24:MI:SS');
        ALTER TABLE tmp_driver ALTER COLUMN rescinded_date TYPE TIMESTAMP USING TO_TIMESTAMP(rescinded_date, 'YY-MM-DD HH24:MI:SS');
        ALTER TABLE tmp_driver ALTER COLUMN first_itinerary_created TYPE TIMESTAMP USING TO_TIMESTAMP(first_itinerary_created, 'YY-MM-DD HH24:MI:SS');

        /* first time select into driver */
        SELECT * INTO driver FROM tmp_driver;

        DROP TABLE tmp_driver;

        SELECT * from driver limit 5;
    """

    copy_cmd = """COPY tmp_driver FROM '{0}' WITH (format csv, header true, delimiter ',');""".format(files[fn])
    # if exists compressed version of file    
    if sys.platform == 'win32' and os.path.exists(files[fn] + '.gz'):
        # path to 7zip
        seven_zip = which('7z')
        if seven_zip == None:
            print('WARNING: can not locate program 7z to copy compressed file into DB')
            print('- In Windows, Postgre can not handle big plain CSV files!')
            print('- It is probabily that this uploading ends in an exception.')
        else:
            copy_cmd = """COPY tmp_driver FROM PROGRAM '"{0}" e -so "{1}"' DELIMITER ',' CSV HEADER;""".format(seven_zip, files[fn] + '.gz')

    df = utils.run_query(create_table_from_csv.format(copy_cmd), df=False)

    df = utils.run_query("""select * from driver limit 5;""")
    if len(df) == 5:
        print('File {} loaded!'.format(fn))

print('Counting rows in driver...')
df = utils.run_query("""SELECT COUNT(1) FROM driver""")
print('Total rows found: {}'.format(df.iloc[0,0]))

print('Creating simple indexes for table driver (slow process)...')

create_simple_index_tpl = 'CREATE INDEX {0}_aidx5 ON driver USING btree ({0});'

for idx in ['first_itinerary_id', 'driver_id']:
    print('Creating index "{}_aidx2"...'.format(idx))
    r = utils.run_query(create_simple_index_tpl.format(idx), df=False)

print('[TODO]: we need to evaluate the creation of better indexes based in our requirements.')

df = utils.run_query("""SELECT pg_size_pretty(pg_database_size(current_database())) as size""")
print('Current DB Size: {}'.format(df.iloc[0,0]))

print('PROCESS FINISHED!')