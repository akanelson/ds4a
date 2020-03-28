import requests
import json
from datetime import timedelta, date, datetime as dt
from practicum_config import dark_sky_api

########################################################################################################
#
# Get weather data from Dark Sky API Service https://darksky.net/dev
#
# Receives: API Key, latitude, longitude, stsart date, end date (end date included) 
# Returns: Dictionary with key: value where key is the date and value is the API response for that day
#
# Sample call:
# dark_sky_get('[YOUR-API-KEY]', -23.5475006, -46.6361084, '2001-01-01 00:00:00', '2001-01-16 00:00:00')
#
########################################################################################################
def dark_sky_get(key, lat, lon, start_date, end_date):
    params = {'exclude': 'currently,hourly,flags'}
    # Convert dates to the format required by the API
    #start_date = dt.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    start_date = dt.strptime(start_date, '%Y-%m-%d')
    #end_date = dt.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    end_date = dt.strptime(end_date, '%Y-%m-%d')
    # Define weather dictionary variable
    data = {}
    # For each day on the range
    for n in range(int((end_date - start_date).days) + 1):
        day = start_date + timedelta(n)
        day = day.strftime("%Y-%m-%dT%H:%M:%S")
        # Build URL
        url = 'https://api.darksky.net/forecast/{}/{},{},{}'.format(key, lat, lon, day)
        print('Getting weather data for day ' + day + ' ...')
        # Get API data
        response = requests.get(url, params)
        json_response = response.json()
        # Add new item to the dictionary only with the needed keys reutned from the API
        data[day] = json_response['daily']['data'][0]

    return data

# San Pablo, Brazil, Latitude and Longitude
latitude = -23.5475006
longitude = -46.6361084
# From date to date range
from_date = '2019-10-01'
to_date = '2020-03-12'
#print(from_date[:10])
# Get data
data = dark_sky_get(dark_sky_api, latitude, longitude, from_date, to_date)
print('Writing file ...')
# Write json to file
with open('../data/weather_daily_' + from_date[:10] + '_' + to_date[:10] +'.json', 'w') as outfile:
    json.dump(data, outfile)
print('Process complete!')
