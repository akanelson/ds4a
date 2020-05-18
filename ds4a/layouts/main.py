import dash_html_components as html
import dash_core_components as dcc
from ds4a.layouts.header import header
from ds4a.components.analytics import analitycs
from ds4a.layouts.tabs import tabs
from ds4a.layouts.inputs import layout_inputs



metrics = [
    {'label': 'Users', 'value': '454', 'tendency_arrow': 'down', 'tendency_value': '6.6%', 'tendency_color': 'red', 'selected': 'true', 'figure_model': 'user_model'},
    {'label': 'Sessions', 'value': '873', 'tendency_arrow': 'down', 'tendency_value': '61.9%', 'tendency_color': 'red', 'selected': 'false', 'figure_model': 'sessions_model'},
    {'label': 'Bounce Rate', 'value': '42.61%', 'tendency_arrow': 'down', 'tendency_value': '9.3%', 'tendency_color': 'green', 'selected': 'false', 'figure_model': 'bounce_rate_model'},
    {'label': 'Session Duration', 'value': '3m 37s', 'tendency_arrow': 'down', 'tendency_value': '2.6%', 'tendency_color': 'red', 'selected': 'false', 'figure_model': 'session_duration_model'},
]

metrics2 = [
    {'label': 'Users2', 'value': '454', 'tendency_arrow': 'down', 'tendency_value': '6.6%', 'tendency_color': 'red', 'selected': 'true'},
    {'label': 'Sessions2', 'value': '873', 'tendency_arrow': 'down', 'tendency_value': '61.9%', 'tendency_color': 'red', 'selected': 'false'},
    {'label': 'Bounce Rate2', 'value': '42.61%', 'tendency_arrow': 'down', 'tendency_value': '9.3%', 'tendency_color': 'green', 'selected': 'false'},
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
                        #html.Div([analitycs(metrics2)],className=""),
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