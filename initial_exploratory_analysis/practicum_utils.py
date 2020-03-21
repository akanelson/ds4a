import practicum_config as config
import pandas as pd
import random
from sqlalchemy import create_engine, text


# utils functions to work with first data availale
dir_data = '../data/supply/'

def get_loggi_files():
	files = [
	    'availability_dist1_ano.csv',
	    'availability_dist2_ano.csv',
	    'itinerary_dist1_ano.csv',
	    'itinerary_dist2_ano.csv'
	]
	return [dir_data + f for f in files]

def read_csv_percent(filename, percent):
    # keep the header and the 'percent' of lines
    return pd.read_csv(
         filename,
         header=0, 
         skiprows=lambda i: i > 0 and random.random() > percent/100
    )

def read_csv_every(filename, k):
    # keep the header and the lines at multiple of k locations
     return pd.read_csv(filename, header=0, skiprows=lambda i: i % k != 0)

# connect to postgre db or throw an error
def global_connect():
    global db
    db = create_engine(config.postgre_conn, max_overflow=20)

def run_query(sql, df=True):
    result = db.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(sql)))
    if df:
        return pd.DataFrame(result.fetchall(), columns=result.keys())
    return result
