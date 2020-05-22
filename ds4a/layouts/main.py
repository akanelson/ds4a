import dash_html_components as html
import dash_core_components as dcc
from ds4a.layouts.header import header
from ds4a.components.analytics import analitycs
from ds4a.layouts.tabs import tabs
from ds4a.layouts.inputs import layout_inputs



range_daily_past = {'Yesterday': 1, 'Last week': 7, 'Last 2 weeks': 14, 'Last 4 weeks': 28}
range_daily_future = {'Next week': 7, 'Next 2 weeks': 14, 'Next 4 weeks': 28}
range_hourly_future = {'Next 6 hours': 6, 'Next 12 hours': 12, 'Next 24 hours': 24, 'Next 48 hours': 48}

config = {'title': 'History - Daily Drivers (both agencies)', 'range_selector': range_daily_past}
metrics = [
    {'label': 'Agency 1 Drivers', 'selected': 'true', 'model': 'drivers_model_a1'},
    {'label': 'Agency 1 Effective Drivers', 'selected': 'false', 'model': 'drivers_model_a1_alo'},
    {'label': 'Agency 2 Drivers', 'selected': 'false', 'model': 'drivers_model_a2'},
    {'label': 'Agency 2 Effective Drivers', 'selected': 'false', 'model': 'drivers_model_a2_alo'},
]
widget = [metrics, config]

config2 = {'title': 'History - Daily Itineraries (both agencies)', 'range_selector':range_daily_past}
metrics2 = [
    {'label': 'Agency 1 Daily Itineraries', 'selected': 'true', 'model': 'itineraries_model_a1'},
    {'label': 'Agency 2 Daily Itineraries', 'selected': 'true', 'model': 'itineraries_model_a2'},
]
widget2 = [metrics2, config2]

config3 = {'title': 'Prediction - Daily Drivers (both agencies)', 'range_selector':range_daily_future}
metrics3 = [
    {'label': 'A1 daily Drivers Prediction', 'selected': 'true', 'model': 'predict_daily_drivers_model_a1'},
    {'label': 'A1 daily Effective Drivers Prediction', 'selected': 'true', 'model': 'predict_daily_drivers_model_a1_alo'},
    {'label': 'A2 daily Drivers Prediction', 'selected': 'true', 'model': 'predict_daily_drivers_model_a2'},
    {'label': 'A2 daily Effective Drivers Prediction', 'selected': 'true', 'model': 'predict_daily_drivers_model_a2_alo'},
]
widget3 = [metrics3, config3]

config4 = {'title': 'Prediction - Hourly Drivers (both agencies)', 'range_selector':range_hourly_future}
metrics4 = [
    {'label': 'A1 hourly Drivers Prediction', 'selected': 'true', 'model': 'predict_hourly_drivers_model_a1'},
    {'label': 'A2 hourly Drivers Prediction', 'selected': 'true', 'model': 'predict_hourly_drivers_model_a2'},    
]
widget4 = [metrics4, config4]

config5 = {'title': 'Prediction - Hourly Drivers (both agencies)', 'range_selector':range_hourly_future}
metrics5 = [
    {'label': 'A1 hourly Drivers ALO Prediction', 'selected': 'true', 'model': 'predict_hourly_drivers_model_a1_alo'},
    {'label': 'A2 hourly Drivers ALO Prediction', 'selected': 'true', 'model': 'predict_hourly_drivers_model_a2_alo'},    
]
widget5 = [metrics5, config5]


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
                        html.Div([analitycs(widget4)],className=""),
                        html.Div([analitycs(widget5)],className=""),
                        html.Div([analitycs(widget3)],className=""),
                        html.Div([analitycs(widget)],className=""),
                        html.Div([analitycs(widget2)],className=""),

                    ],
                    className="col-lg-9 col-12" 
                ),
            ],
            className="row"
        ),
#        html.Div(
#            html.Div(
#                tabs,
#                className="col-lg-9 col-12"
#            ),
#            className="row"
#        ),
    ],
    className="container-fluid"
)