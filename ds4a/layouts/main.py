import dash_html_components as html
import dash_core_components as dcc
from ds4a.layouts.header import header
from ds4a.components.analytics import analitycs
from ds4a.layouts.tabs import tabs
from ds4a.layouts.inputs import layout_inputs



metrics = [
    {'label': 'Users', 'selected': 'true', 'model': 'user_model'},
    {'label': 'Sessions', 'selected': 'false', 'model': 'sessions_model'},
    {'label': 'Bounce Rate', 'selected': 'false', 'model': 'bounce_rate_model'},
    {'label': 'Session Duration', 'selected': 'false', 'model': 'session_duration_model'},
]

metrics2 = [
    {'label': 'Users2', 'selected': 'true', 'model': 'user2_model'},
    {'label': 'Sessions2', 'selected': 'false', 'model': 'sessions2_model'},
    {'label': 'Bounce Rate2', 'selected': 'false', 'model': 'bounce_rate2_model'},
]

main_layout = html.Div(
    [
        html.Div(header, className=''),
        html.Div(
            [
                html.Div(
                    html.Div(
                        [
                            html.H1("Controls", className='title'),
                            layout_inputs
                        ],
                        className='controls',
                        id='controls'
                    ),
                    className="col-lg-3 col-12"
                ),
                html.Div(
                    [
                        html.Div([analitycs(metrics)],className=""),
                        html.Div([analitycs(metrics2)],className=""),
                    ],
                    className="col-lg-9 col-12" 
                ),
            ],
            className="row"
        ),
        html.Div(
            html.Div(
                tabs,
                className="col-lg-9 col-12"
            ),
            className="row"
        ),
    ],
    className="container-fluid"
)