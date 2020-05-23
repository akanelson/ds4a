import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from ds4a.layouts.header import header
from ds4a.components.analytics import analitycs
from ds4a.layouts.tabs import tabs
from ds4a.layouts.inputs import layout_inputs


range_daily_past = {'Yesterday': 1, 'Last week': 7, 'Last 2 weeks': 14, 'Last 4 weeks': 28}
range_hourly_past = {'Last 2 days': 24, 'Last week': 24*7, 'Last 2 weeks': 24*14, 'Last month': 24*28}
range_daily_future = {'Next week': 7, 'Next 2 weeks': 14, 'Next 4 weeks': 28}
range_hourly_future = {'Next 6 hours': 6, 'Next 12 hours': 12, 'Next 24 hours': 24, 'Next 48 hours': 48}

config = {'title': 'Daily Metrics', 'range_selector': range_daily_past, 'wrapper_type': 'historical'}
metrics = [
    {'label': 'All Drivers', 'selected': 'true', 'model': 'drivers_model', 'help': 'All Drivers of the selected period vs the previous period. Mean Drivers for the selected period. Tendency between mean`s current period and previous period.'},
    {'label': 'Effective Drivers', 'selected': 'false', 'model': 'drivers_model_alo', 'help': 'Drivers who worked at leats once for the current agency of the selected period vs the previous period. Mean Drivers for the selected period. Tendency between mean`s current period and previous period.'},
    {'label': 'Itineraries', 'selected': 'false', 'model': 'itineraries_model'}
]
widget_history_daily = [metrics, config]

config2 = {'title': 'Hourly Metrics', 'range_selector': range_hourly_past, 'wrapper_type': 'historical'}
metrics2 = [
    {'label': 'All Drivers', 'selected': 'true', 'model': 'hourly_drivers_model'},
    {'label': 'Effective Drivers', 'selected': 'false', 'model': 'hourly_drivers_model_alo'},
    {'label': 'Itineraries', 'selected': 'false', 'model': 'hourly_itineraries_model'}
]
widget_history_hourly = [metrics2, config2]

config3 = {'title': 'Daily Drivers', 'range_selector': range_daily_future, 'wrapper_type': 'prediction'}
metrics3 = [
    {'label': 'All Drivers Forecast', 'selected': 'true', 'model': 'predict_daily_drivers_model'},
    {'label': 'Effective Drivers Forecast', 'selected': 'true', 'model': 'predict_daily_drivers_model_alo'}
]
widget_prediction_daily = [metrics3, config3]

config4 = {'title': 'Hourly Drivers Forecast', 'range_selector': range_hourly_future, 'wrapper_type': 'prediction'}
metrics4 = [
    {'label': 'All Drivers Forecast', 'selected': 'true', 'model': 'predict_hourly_drivers_model'},
    {'label': 'Effective Drivers Forecast', 'selected': 'false', 'model': 'predict_hourly_drivers_model_alo'},
]
widget_prediction_hourly = [metrics4, config4]

config5 = {'title': 'Real Time', 'range_selector': {'Today': 24}, 'wrapper_type': 'real_time'}
metrics5 = [{'label': 'Agency Snapshot', 'selected': 'true', 'model': 'realtime_itineraries_model'}]
widget_realtime = [metrics5, config5]

main_layout = html.Div(
    [
        html.Div(header, className=''),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.NavLink([html.I('', className="fas fa-history"), 'Historical'], href="#", className='menu-item', id='historical')),
                                dbc.NavItem(dbc.NavLink([html.I('', className="fas fa-clock"), 'Real Time'], href="#", active=True, className='menu-item', id='real_time')),
                                dbc.NavItem(dbc.NavLink([html.I('', className="fas fa-brain"), 'Forecast'], href="#", className='menu-item', id='prediction')),
                            ],
                            vertical="md",
                            pills=True
                        ),                        
                        html.Div(
                            [
                                html.H1("Controls", className='title'),
                                layout_inputs
                            ],
                            className='controls',
                            id='controls'
                        ),
                    ],
                    className="col-lg-2 col-12 wrapper-controls"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div([analitycs(widget_history_daily)],className="col-lg-6 col-12"),
                                html.Div([analitycs(widget_history_hourly)],className="col-lg-6 col-12"),
                            ],
                            className='row',
                            id='wrapper-historical'
                        ),
                        html.Div(
                            [
                                html.Div([analitycs(widget_realtime)],className="col-lg-6 col-12"),
                                html.Div([analitycs(widget_realtime)],className="col-lg-6 col-12"),
                            ],
                            className='row',
                            id='wrapper-realtime'
                        ),
                        html.Div(
                            [
                                html.Div([analitycs(widget_prediction_daily)],className="col-lg-6 col-12"),
                                html.Div([analitycs(widget_prediction_hourly)],className="col-lg-6 col-12"),
                            ],
                            className='row',
                            id='wrapper-forecast'
                        ),
                    ],
                    className="col-lg-10 col-12" 
                ),
            ],
            className="row"
        ),
    ],
    className="container-fluid"
)