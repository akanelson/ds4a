import dash_html_components as html
import dash_core_components as dcc
from datetime import datetime as dt

layout_inputs = html.Div([
    html.H3("Inputs"),

    html.Div(
        [
            dcc.DatePickerSingle(
                id='input-current-date',
                min_date_allowed=dt(2019, 8, 1),
                max_date_allowed=dt(2020, 3, 31),
                initial_visible_month=dt(2019, 8, 1),
                date=str(dt(2019, 11, 12)),
                with_portal=False,
                className='input-current-date'
            ),

            dcc.Dropdown(
                id='input-current-hour',
                options=[
                    {'label': '00:00', 'value': '0'},
                    {'label': '01:00', 'value': '1'},
                    {'label': '02:00', 'value': '2'},
                    {'label': '03:00', 'value': '3'},
                    {'label': '04:00', 'value': '4'},
                    {'label': '05:00', 'value': '5'},
                    {'label': '06:00', 'value': '6'},
                    {'label': '07:00', 'value': '7'},
                    {'label': '08:00', 'value': '8'},
                    {'label': '09:00', 'value': '9'},
                    {'label': '10:00', 'value': '10'},
                    {'label': '11:00', 'value': '11'},
                    {'label': '12:00', 'value': '12'},
                    {'label': '13:00', 'value': '13'},
                    {'label': '14:00', 'value': '14'},
                    {'label': '15:00', 'value': '15'},
                    {'label': '16:00', 'value': '16'},
                    {'label': '17:00', 'value': '17'},
                    {'label': '18:00', 'value': '18'},
                    {'label': '19:00', 'value': '19'},
                    {'label': '20:00', 'value': '20'},
                    {'label': '21:00', 'value': '21'},
                    {'label': '22:00', 'value': '22'},
                    {'label': '23:00', 'value': '23'},
                ],
                value='15',
                clearable=False,
                className="input-current-hour"
            ),
        ],
        className="row"
    ),
    
    html.Div(children=[
        html.Div(children=[
            html.Label("Mean"),
            dcc.Input(id="input-mean", type="number", className="form-control", value="0")
        ]),
    ], className="row"),
    html.Div(children=[
        html.Div(children=[
            html.Label("Standard Deviation"),
            dcc.Input(id="input-stdv", type="number", className="form-control", value="1")
        ]),
    ], className="row"),
])