import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from datetime import datetime
from datetime import timedelta
from practicum_utils import get_loggi_files, global_connect, run_query, explained_time, careful_query
import numpy as np
from ds4a.components.carta import *
import ds4a.models.analytics_utils as au
import plotly.colors as colors



# ----------------------
# hard coded agencies ID
# ----------------------
agency = {'1': '6e7dacf2149d053183fe901e3cfd8b82', '2': '58cfe3b975dd7cbd1ac84d555640bfd9'}


def realtime_map(current_date=None, current_time=None, current_agency=None):

    
    carta_1 = create_div_carta(arr = [0], label="---")
    carta_2 = create_div_carta(arr = [0], label="---")

    if current_date != None:
        now = current_date[:10] + ' ' + current_time
        df = au.get_hourly_drivers(agency[current_agency], current_date, now)
        #print('drivers', df.shape)

        carta_1 = create_div_carta(arr = df['drivers'].values, label="Drivers in area",
            fmt='{:.0f} drivers',
            help='Number of unique drivers found in agency area in last hour.')

        carta_2 = create_div_carta(arr = df['drivers_alo'].values, label="Effective drivers",
            fmt='{:.0f} effective drivers',
            help='Number of effective drivers found in agency area in last hour. By effective driver we mean a driver who has worked at least once in the past for the agency.')

    carta_drivers = html.Div(carta_1, className='col-lg-6 carta-drivers') # col-md-4 col-sm-6 col-6
    carta_effective_drivers = html.Div(carta_2, className='col-lg-6 carta-effective-drivers')

    markup = dcc.Loading(
    [   
        html.Div(
                [
                    html.Div('Snapshot geographical distribution of drivers', className='analytics-title'),
                    html.Div([carta_drivers, carta_effective_drivers], className='row'),
                    html.Div(get_map(current_date, current_time, current_agency), className='map-wrapper')
                ],
                id='realtime-map',
                className="geo-wrapper",
        )
    ], id='loading-map', className='analytics-loading')
    return markup


def get_map(current_date, current_time, current_agency):

    lat, lng = np.array([0]), np.array([0])

    if current_date != None:
        today = current_date[:10] + ' ' + current_time
        now = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        from_ = now - timedelta(minutes=int(5))
        #print(now, from_)

        df = careful_query("""
            select driver_id, avg(lat) as lat, avg(lng) as lng
            from availability a 
            where sent_f =  '{1}'
            --and sent_f <= '{1}'
            and distribution_center = '{0}'
            group by driver_id
        """.format(agency[current_agency], str(now), str(from_)))

        print('available rows:', len(df))

        print(df.shape)
        #df = df.groupby('driver_id')[['lat', 'lng']].mean()
        df = df[['lat', 'lng']]
        print(df.shape)
        lat = df['lat']
        lng = df['lng']


    if 1==1:
        fig = go.Figure()
        # Reference for colorscales: https://plotly.com/python/builtin-colorscales/
        fig.add_trace(go.Densitymapbox(lat=lat, lon=lng, radius=10, colorscale=colors.sequential.PuBu_r))
    else:
        fig = go.Figure(go.Scattermapbox(
                lat=lat,
                lon=lng,
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=9
                ),
            ))

    fig.update_geos(fitbounds="locations")
    
    fig.update_layout(
        margin = {'l':0,'t':0,'b':0,'r':0},
        mapbox = {
        #'accesstoken': 'TOKEN',
        'center': {'lat': lat.mean(), 'lon': lng.mean()},
        'style': 'carto-positron', #'open-street-map',
        'zoom': 11})



    return html.Div([
        dcc.Graph(figure=fig)
    ])