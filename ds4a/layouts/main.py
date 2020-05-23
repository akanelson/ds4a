import dash_html_components as html
import dash_core_components as dcc
from ds4a.layouts.header import header
from ds4a.components.analytics import analitycs
from ds4a.layouts.tabs import tabs
from ds4a.layouts.inputs import layout_inputs


range_daily_past = {'Yesterday': 1, 'Last week': 7, 'Last 2 weeks': 14, 'Last 4 weeks': 28}
range_hourly_past = {'Last 2 days': 24, 'Last week': 24*7, 'Last 2 weeks': 24*14, 'Last month': 24*28}
range_daily_future = {'Next week': 7, 'Next 2 weeks': 14, 'Next 4 weeks': 28}
range_hourly_future = {'Next 6 hours': 6, 'Next 12 hours': 12, 'Next 24 hours': 24, 'Next 48 hours': 48}

config = {'title': 'History - Daily Agency Metrics', 'range_selector': range_daily_past}
metrics = [
    {'label': 'Drivers', 'selected': 'true', 'model': 'drivers_model', 'help': 'All Drivers of the selected period vs the previous period. Mean Drivers for the selected period. Tendency between mean`s current period and previous period.'},
    {'label': 'Effective Drivers', 'selected': 'false', 'model': 'drivers_model_alo', 'help': 'Drivers who worked at leats once for the current agency of the selected period vs the previous period. Mean Drivers for the selected period. Tendency between mean`s current period and previous period.'},
    {'label': 'Daily Itineraries', 'selected': 'false', 'model': 'itineraries_model'}
]
widget_history_daily = [metrics, config]

config2 = {'title': 'History - Hourly Agency Metrics', 'range_selector': range_hourly_past}
metrics2 = [
    {'label': 'Drivers', 'selected': 'true', 'model': 'hourly_drivers_model'},
    {'label': 'Effective Drivers', 'selected': 'false', 'model': 'hourly_drivers_model_alo'},
    {'label': 'Itineraries', 'selected': 'false', 'model': 'hourly_itineraries_model'}
]
widget_history_hourly = [metrics2, config2]

config3 = {'title': 'Prediction - Daily Drivers per Agency', 'range_selector': range_daily_future}
metrics3 = [
    {'label': 'Drivers Prediction', 'selected': 'true', 'model': 'predict_daily_drivers_model'},
    {'label': 'Effective Drivers Prediction', 'selected': 'true', 'model': 'predict_daily_drivers_model_alo'}
]
widget_prediction_daily = [metrics3, config3]

config4 = {'title': 'Prediction - Hourly Drivers per Agency', 'range_selector': range_hourly_future}
metrics4 = [
    {'label': 'Drivers Prediction', 'selected': 'true', 'model': 'predict_hourly_drivers_model'},
    {'label': 'Effective Drivers Prediction', 'selected': 'false', 'model': 'predict_hourly_drivers_model_alo'},
]
widget_prediction_hourly = [metrics4, config4]

widget_realtime = [
    [{'label': 'Agency Snapshot', 'selected': 'true', 'model': 'realtime_itineraries_model'}],
    {'title': 'Agency - Realtime', 'range_selector': {'fix': 24}}
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
                        html.Div([analitycs(widget_history_daily)],className=""),
                        html.Div([analitycs(widget_history_hourly)],className=""),
                        html.Div([analitycs(widget_realtime)],className=""),
                        html.Div([analitycs(widget_prediction_daily)],className=""),
                        html.Div([analitycs(widget_prediction_hourly)],className=""),
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