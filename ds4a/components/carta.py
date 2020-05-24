import numpy as np
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go
import random
import time
# Now we can import our modulue
import practicum_utils as utils
import ds4a.models.analytics_utils as au
from datetime import datetime, timedelta


def create_div_carta(arr, label='', fmt='{:.2f}', help='No info'):
    """Create a carta component (DIV) using the last value of the array"""
    """(arr[-1]) and creating a line with the array values at arr"""

    USE_MARKERS = False

    n = len(arr)

    # Create figure line
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.linspace(0, 1, n), y=arr,
        mode='lines+markers' if USE_MARKERS else 'lines',
        line=dict(color='#00baff', width=2),
        fill='tozeroy',
        hoverinfo='none',
        ))
    # Define layout where line is shown
    fig.update_layout(
        autosize=True,
        height=30,
        yaxis=dict(ticktext=[], tickvals=[]),
        xaxis=dict(ticktext=[], tickvals=[]),
        margin=dict(l=5, r=5, b=5, t=5),
        plot_bgcolor='#ffffff',
        paper_bgcolor="#ffffff",
    )

    # Build value and apply format
    if fmt == 'time':
        value = time.strftime('%H:%M:%S', time.gmtime(int(arr[-1])))
    else:
        value = fmt.format(arr[-1])

    # return CARTA DIV component
    return html.Div(
        className = 'wx_carta ',
        children =[
            html.Div(
                [
                    html.I(className="fas fa-question-circle fa-lg"),
                    html.Span(help, className='tooltip-text'),
                ],
                className='tooltip-wrapper'
            ),
            html.Span(label, className='label'),
    		html.H3(value, className='value'),
    		dcc.Graph(figure=fig, config={'displayModeBar': False}, className='sparkline'),
    	],
	)

def realtime_cartas(current_date=None, current_time=None, current_agency=None):

    
    carta_1 = html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*3600)+5612, label='---', fmt='time', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        )

    carta_2 = html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='---', fmt='time', help='Lorem ipsum dolor sit amet consectetur adipiscing elit.'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        )

    carta_3 = html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='---', fmt='{:.2f}', help='Quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        )
    carta_4 = html.Div(
            create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='---', fmt='{:.2f}', help='Lorem ipsum dolor.'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        )

    if current_date != None:
        now = current_date[:10] + ' ' + current_time
        carta_1, carta_2, carta_3, carta_4 = cartas_realtime_itineraries(now, ag=current_agency)
    
    markup = dcc.Loading(children=
        [   
            html.Div([carta_1, carta_2, carta_3, carta_4], className='row')
        ],
        id='loading-cartas',
        className='analytics-loading'
    )
    
    return markup
    

def cartas_realtime_itineraries(current_date_time, ag):

    print('current_date_time', current_date_time)

    df = au.get_hourly_day_itineraries(au.agency[ag], current_date_time)

    df = df.fillna(0)
    #arr = df['finished_avg_time'].apply(lambda x: str(timedelta(seconds=int(x)))).values
    arr_1 = df['finished_avg_time'].astype('int').values
    #arr_2 = df['created_to_accept_avg_time'].astype('int').values
    arr_3 = df['finished_cumsum'].astype('int').values
    arr_4 = df['pending_acceptance'].astype('int').values
    arr_5 = (df['pending'] - df['pending_acceptance']).astype('int').values

    #print(len(arr_1), len(arr_2))

    c1 = html.Div(
            create_div_carta(arr = arr_1, label='Itinerary completion time', fmt='time', help='Average time to finish a delivery'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        )
        #c2 = html.Div(
    #        create_div_carta(arr = arr_2, label='Avg Time to be Accepted', fmt='time', help='Average time of an itinerary to be accepted'),
    #        className='col-lg-3 col-md-4 col-sm-6 col-6'
    #    )

    c3 = html.Div(
            create_div_carta(arr = arr_3, label='Itineraries finished', fmt='{} units', help='Number of Deliveries Done'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        )

    c4 = html.Div(
            create_div_carta(arr = arr_4, label='Itineraries pending acceptance', fmt='{} units', help='Number of itineraries pending to be accepted right now'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        )

    c5 = html.Div(
            create_div_carta(arr = arr_5, label='Itineraries in-progress', fmt='{} units', help='Number of active deliveries'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        )



    return c1, c3, c4, c5