import dash_core_components as dcc
import dash_html_components as html

def realtime_map(current_date=None, current_time=None, current_agency=None):
    markup = dcc.Loading(
    [   
        html.Div(
                [
                    html.Div('Snapshot geographical distribution', className='analytics-title'),
                    'Hola mapa'
                ],
                id='realtime-map',
                className="map-wrapper",
        )
    ], id='loading-map', className='analytics-loading')
    return markup