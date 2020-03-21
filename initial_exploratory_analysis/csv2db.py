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
        created         TEXT,
        accepted        TEXT,
        dropped         TEXT,
        started         TEXT,
        finished        TEXT,
        status          VARCHAR(30),
        total_distance  FLOAT NOT NULL,
        transport_type  VARCHAR(20) NOT NULL,
        product         VARCHAR(20) NOT NULL,
        product_version VARCHAR(20) NOT NULL,
        distribution_center1    INT NOT NULL,
        packages        FLOAT,
        delivered_packages      FLOAT,
        checked_in_at       TEXT,
        pickup_checkout_at  TEXT,
        pickup_lat          FLOAT,
        pickup_lng          FLOAT,
        real_completion_time    FLOAT,
        pickup_distance     INT,
        pickup_time         TEXT,
        check_in_time       TEXT,
        waypoints           INT
    );
    COPY itineraries FROM '""" + os.path.abspath(files[2]) + """' WITH (format csv, header true, delimiter ',');
    ALTER TABLE itineraries ADD PRIMARY KEY (itinerary_id);
    COPY itineraries FROM '""" + os.path.abspath(files[3]) + """' WITH (format csv, header true, delimiter ',');
    ALTER TABLE itineraries DROP COLUMN temp;
    SELECT * FROM itineraries LIMIT 5;
    """)

    if len(df) == 5:
        print('TABLE itineraries created and data was loaded!')

    # Check if table already exists
    df = run_query("""select t.table_name FROM information_schema.tables as t WHERE t.table_name = 'availabilities'""")
    if len(df) == 1:
        print('Table availabilities already exists')
        if len(sys.argv) > 1 and sys.argv[1] == 'drop':
            print('Forced drop...')
            run_query("""DROP TABLE availabilities""", df=False)
        else:
            exit()

    print('Creating table availabilities and loading csv files. This will take some time...')

    create_table_from_csv = """
    CREATE TABLE availabilities
    (
        temp            TEXT,
        id              VARCHAR(32) NOT NULL,
        driver_id       VARCHAR(32),
        itinerary_id    VARCHAR(32),
        lat             FLOAT,
        lng             FLOAT,
        sent            TEXT,
        transport_type  INT
    );
    COPY availabilities FROM '{0}' WITH (format csv, header true, delimiter ',');
    COPY availabilities FROM '{1}' WITH (format csv, header true, delimiter ',');
    /* ALTER TABLE availabilities ADD PRIMARY KEY (id); */
    ALTER TABLE availabilities DROP COLUMN temp;
    SELECT * from availabilities limit 5;
    """

    df = run_query(create_table_from_csv.format(
                        os.path.abspath(files[0]),
                        os.path.abspath(files[1])), df=False)

    df = run_query("""select * from availabilities limit 5;""")
    if len(df) == 5:
        print('TABLE availabilities created and data was loaded!')