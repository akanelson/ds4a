from practicum_utils import get_loggi_files, global_connect, run_query
import pandas as pd
import os
import sys

if __name__ == "__main__":

    show_usage = False
    if len(sys.argv) == 1:
        show_usage = True        
    elif sys.argv[1] not in ['up', 'drop']:
        print('Invalid usage!')
        show_usage = True

    if show_usage:
        print('-'*72)
        print("This file will create tables itineraries and availabilities in postgre db from Loggi's cvs files")
        print('USAGE:')
        print('- Create tables and upload files if tables not exist')
        print('  #> python csv2db.py up')
        print('- Create tables and upload files dropping tables if they exist')
        print('  #> python csv2db.py drop')
        print('-'*72)
        exit()

    global_connect()

    # check if Loggi's csv files exists or exit because not assertion
    files = get_loggi_files()
    for f in files:
    	assert(os.path.exists(f)==True)

    # -----------
    # ITINERARIES
    # -----------

    # Check if table already exists
    df = run_query("""select t.table_name FROM information_schema.tables as t WHERE t.table_name = 'itineraries'""")
    if len(df) == 1:
        print('Table itineraries already exists')
        if len(sys.argv) > 1 and sys.argv[1] == 'drop':
            print('Forced drop...')
            run_query("""DROP TABLE itineraries""", df=False)
        else:
            exit()

    print('Creating table itineraries and loading csv files...')

    df = run_query("""
    CREATE TABLE itineraries
    (
        temp            TEXT,
        itinerary_id    VARCHAR(32) NOT NULL,
        driver_id       VARCHAR(32),
        created         VARCHAR(14),
        accepted        VARCHAR(14),
        dropped         VARCHAR(14),
        started         VARCHAR(14),
        finished        VARCHAR(14),
        status          VARCHAR(30),
        total_distance  FLOAT NOT NULL,
        transport_type  VARCHAR(20) NOT NULL,
        product         VARCHAR(20) NOT NULL,
        product_version VARCHAR(20) NOT NULL,
        distribution_center1    INT NOT NULL,
        packages        FLOAT,
        delivered_packages      FLOAT,
        checked_in_at       VARCHAR(14),
        pickup_checkout_at  VARCHAR(14),
        pickup_lat          FLOAT,
        pickup_lng          FLOAT,
        real_completion_time    FLOAT,
        pickup_distance     INT,
        pickup_time         FLOAT,
        check_in_time       FLOAT,
        waypoints           INT
    );
    COPY itineraries FROM '""" + os.path.abspath(files[2]) + """' WITH (format csv, header true, delimiter ',');
    ALTER TABLE itineraries ADD PRIMARY KEY (itinerary_id);
    COPY itineraries FROM '""" + os.path.abspath(files[3]) + """' WITH (format csv, header true, delimiter ',');
    ALTER TABLE itineraries DROP COLUMN temp;
    ALTER TABLE itineraries ALTER COLUMN created TYPE TIMESTAMP USING TO_TIMESTAMP(created, 'YY-MM-DD H24:SS');
    ALTER TABLE itineraries ALTER COLUMN accepted TYPE TIMESTAMP USING TO_TIMESTAMP(accepted, 'YY-MM-DD H24:SS');
    ALTER TABLE itineraries ALTER COLUMN dropped TYPE TIMESTAMP USING TO_TIMESTAMP(dropped, 'YY-MM-DD H24:SS');
    ALTER TABLE itineraries ALTER COLUMN started TYPE TIMESTAMP USING TO_TIMESTAMP(started, 'YY-MM-DD H24:SS');
    ALTER TABLE itineraries ALTER COLUMN finished TYPE TIMESTAMP USING TO_TIMESTAMP(finished, 'YY-MM-DD H24:SS');
    ALTER TABLE itineraries ALTER COLUMN checked_in_at TYPE TIMESTAMP USING TO_TIMESTAMP(checked_in_at, 'YY-MM-DD H24:SS');
    ALTER TABLE itineraries ALTER COLUMN pickup_checkout_at TYPE TIMESTAMP USING TO_TIMESTAMP(pickup_checkout_at, 'YY-MM-DD H24:SS');
    SELECT * FROM itineraries LIMIT 5;
    """)

    if len(df) == 5:
        print('TABLE itineraries created and data was loaded!')


    print('Counting rows in itineraries...')
    df = run_query("""SELECT COUNT(1) FROM itineraries""")
    print('Total rows found: {}'.format(df.iloc[0,0]))

    print('Creating simple indexes for table itineraries...')

    create_simple_index_tpl = 'CREATE INDEX {0}_iidx ON itineraries USING btree ({0});'

    for idx in ['driver_id', 'created', 'accepted', 'dropped', 'started', 'finished',
                'checked_in_at', 'pickup_checkout_at', 'check_in_time', 'pickup_time',
                'pickup_distance', 'pickup_lat', 'pickup_lng', 'status', 'total_distance',
                'transport_type', 'real_completion_time', 'distribution_center1']:

        print('Creating index "{}_iidx"...'.format(idx))
        r = run_query(create_simple_index_tpl.format(idx), df=False)

    # --------------
    # AVAILABILITIES
    # --------------

    # Check if table already exists
    df = run_query("""select t.table_name FROM information_schema.tables as t WHERE t.table_name = 'availabilities'""")
    if len(df) == 1:
        print('Table availabilities already exists')
        if len(sys.argv) > 1 and sys.argv[1] == 'drop':
            print('Forced drop...')
            run_query("""DROP TABLE availabilities""", df=False)
        else:
            exit()

    tpl = ['SELECT {} as distribution_center, * INTO availabilities FROM tmp_availabilities',
           'INSERT INTO availabilities SELECT {} as distribution_center, * FROM tmp_availabilities']

    for fn, agency, _tpl in [(files[0], 1, tpl[0]), (files[1], 2, tpl[1])]:
        print('Creating temporal table for availabilies.\nLoading csv file {}.\nThis will take some time...'.format(fn))

        create_table_from_csv = """
            CREATE TEMPORARY TABLE tmp_availabilities
            (
                temp            INT,
                id              VARCHAR(32) NOT NULL,
                driver_id       VARCHAR(32),
                itinerary_id    VARCHAR(32),
                lat             FLOAT,
                lng             FLOAT,
                sent            VARCHAR(14),
                transport_type  INT
            );
            COPY tmp_availabilities FROM '{0}' WITH (format csv, header true, delimiter ',');
            ALTER TABLE tmp_availabilities DROP COLUMN temp;
            ALTER TABLE tmp_availabilities ALTER COLUMN sent TYPE TIMESTAMP USING TO_TIMESTAMP(sent, 'YY-MM-DD H24:SS');    

            /* first time select into availabilities, second time insert into availabilities*/
            {1};

            DROP TABLE tmp_availabilities;

            SELECT * from availabilities limit 5;
        """

        df = run_query(create_table_from_csv.format(os.path.abspath(fn), _tpl.format(agency)), df=False)

        df = run_query("""select * from availabilities limit 5;""")
        if len(df) == 5:
            print('File {} loaded!'.format(fn))

    print('Counting rows in availabilities...')
    df = run_query("""SELECT COUNT(1) FROM availabilities""")
    print('Total rows found: {}'.format(df.iloc[0,0]))

    print('Creating simple indexes for table availabilities (slow process)...')

    create_simple_index_tpl = 'CREATE INDEX {0}_aidx ON availabilities USING btree ({0});'

    for idx in ['id', 'distribution_center', 'driver_id', 'itinerary_id', 'sent']:
        print('Creating index "{}_aidx"...'.format(idx))
        r = run_query(create_simple_index_tpl.format(idx), df=False)

    print('[TODO]: we need to evaluate the creation of better indexes based in our requirements.')

    df = run_query("""SELECT pg_size_pretty(pg_database_size(current_database())) as size""")
    print('Current DB Size: {}'.format(df.iloc[0,0]))

    print('PROCESS FINISHED!')