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

    markup = dcc.Loading(
    [   
        html.Div(
                [
                    html.Div("What's the location of the drivers?", className='analytics-title'),
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
        """.format(agency[current_agency], str(now), str(from_)), 1000000)

        print(df.shape)
        df = df[['lat', 'lng']]
        lat = df['lat']
        lng = df['lng']

    if 1==1:
        fig = go.Figure()
        # Reference for colorscales: https://plotly.com/python/builtin-colorscales/
        fig.add_trace(go.Densitymapbox(lat=lat, lon=lng, radius=10, colorscale=colors.sequential.Purp))
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
        hovermode = False,
        margin = {'l':0,'t':0,'b':0,'r':0},
        mapbox = {
        #'accesstoken': 'TOKEN',
        'center': {'lat': lat.mean(), 'lon': lng.mean()},
        'style': 'carto-positron', #'open-street-map',
        'zoom': 11,})



    return html.Div([
        dcc.Graph(figure=fig)
    ])