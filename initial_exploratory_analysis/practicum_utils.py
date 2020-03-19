import pandas as pd
import random

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


# uuuu te rompi todo