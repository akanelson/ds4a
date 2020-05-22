import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt

layout_inputs = html.Div([
    html.H4("Current Date & Time", className='input-title'),
    html.Div(
        [
            dcc.DatePickerSingle(
                id='input-current-date',
                min_date_allowed=dt(2019, 12, 1),
                max_date_allowed=dt(2020, 2, 29),
                initial_visible_month=dt(2020, 2, 10),
                date=str(dt(2020, 2, 10)),
                with_portal=False,
                className='input-current-date'
            ),

            dcc.Dropdown(
                id='input-current-hour',
                options=[
                    {'label': '00:00', 'value': '00:00:00'},
                    {'label': '01:00', 'value': '01:00:00'},
                    {'label': '02:00', 'value': '02:00:00'},
                    {'label': '03:00', 'value': '03:00:00'},
                    {'label': '04:00', 'value': '04:00:00'},
                    {'label': '05:00', 'value': '05:00:00'},
                    {'label': '06:00', 'value': '06:00:00'},
                    {'label': '07:00', 'value': '07:00:00'},
                    {'label': '08:00', 'value': '08:00:00'},
                    {'label': '09:00', 'value': '09:00:00'},
                    {'label': '10:00', 'value': '10:00:00'},
                    {'label': '11:00', 'value': '11:00:00'},
                    {'label': '12:00', 'value': '12:00:00'},
                    {'label': '13:00', 'value': '13:00:00'},
                    {'label': '14:00', 'value': '14:00:00'},
                    {'label': '15:00', 'value': '15:00:00'},
                    {'label': '16:00', 'value': '16:00:00'},
                    {'label': '17:00', 'value': '17:00:00'},
                    {'label': '18:00', 'value': '18:00:00'},
                    {'label': '19:00', 'value': '19:00:00'},
                    {'label': '20:00', 'value': '20:00:00'},
                    {'label': '21:00', 'value': '21:00:00'},
                    {'label': '22:00', 'value': '22:00:00'},
                    {'label': '23:00', 'value': '23:00:00'},
                ],
                value='15:00:00',
                clearable=False,
                className="input-current-hour"
            ),
        ],
        className="row"
    ),

    html.H4("Agency", className='input-title'),
    html.Div(children=[
        dcc.RadioItems(options=[
            {'label': 'Agency 1', 'value': '6e7dacf2149d053183fe901e3cfd8b82'},
            {'label': 'Agency 2', 'value': '58cfe3b975dd7cbd1ac84d555640bfd9'},
            {'label': 'All', 'value': ''}
        ],
        id='input-agency',
        value='6e7dacf2149d053183fe901e3cfd8b82',
        className='input-agency-selector'),
    ], className="row"),

    html.Button(['Refresh Dashboard', html.I('', className="fas fa-refresh", id='input-refresh')], className='input-refresh')
])