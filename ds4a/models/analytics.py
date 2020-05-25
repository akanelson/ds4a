import random
from datetime import datetime
from datetime import timedelta

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Now we can import our modulue
import practicum_utils as utils
import ds4a.models.analytics_utils as au


def drivers_model(date_range, current_date_time, current_agency='1'):
    return base_drivers_model(date_range, current_date_time, current_agency, column='drivers')

def drivers_model_alo(date_range, current_date_time, current_agency='1'):
    return base_drivers_model(date_range, current_date_time, current_agency, column='drivers_alo')

def base_drivers_model(date_range, current_date_time, ag='1', column='drivers'):

    #column = 'drivers' # drivers_alo, drivers_alo_10_days

    #print(date_range, current_date_time)

    to_1 = datetime.strptime(current_date_time[:10], '%Y-%m-%d')
    from_1 = to_1 - timedelta(days=int(date_range))
    to_2 = from_1
    from_2 = to_2 - timedelta(days=int(date_range))
    df1 = au.get_daily_drivers(au.agency[ag], from_1, to_1)
    df2 = au.get_daily_drivers(au.agency[ag], from_2, to_2)

    value1 = df1[column].mean()
    value2 = df2[column].mean()

    trace1 = {
        'x': df1.index,
        'y': df1[column].values,
        'mode': 'lines',
        'name': 'This period',
        'line': {
            'dash': 'solid',
            'width': 2,
            'color': '#00baff'
        }
    }

    if df1.shape == df2.shape:
        df2.set_index(df1.index, inplace=True)
        df2.rename(columns = {col: f"prev_{col}" for col in df2.columns}, inplace=True)
        df = df1.merge(df2, on='date')
        #print(df.columns)
        df = df[[column, 'prev_' + column]]
        #print(df.shape)


        trace2 = {
            'x': df.index,
            'y': df['prev_' + column].values,
            'mode': 'lines',
            'name': 'Previous period',
            'line': {
                'dash': 'dot',
                'width': 2,
                'color': '#00baff'
            }
        }

        data = [trace1, trace2]

    else:
        print('Warning: current vs previous sizes are different! Probably not enought data. Use another date range.')
        data = [trace1]


    layout = {
        'margin': {'b':10, 't':10},    
        'xaxis': {
            'autorange': True,
            'nticks': len(df1.index)
        },
        'yaxis': {
            'autorange': True,
            'title': column
        },
        'legend': {
            'orientation': 'h',
            'xanchor': 'center',
            'y': -.3,
            'x': 0.5,
            'font': {
            'size': 14
            }
        }
    }

    # if yesterday try to use another kind of figure
    if int(date_range) == 1:
        x = ['Yesterday', 'Before yesterday']
        y = [value1, value2]
        figure = go.Figure([go.Bar(x=x, y=y)])
    else:
        figure = {'data': data, 'layout': layout}

    if value1 >= value2:
        tendency_color = 'green'        
        tendency_arrow = 'fa-long-arrow-alt-up'
    else:
        tendency_arrow = 'fa-long-arrow-alt-down'
        tendency_color = 'red'        


    tendency_value = str(abs(round(((value1/(value2+0.001))-1)*100, 2)))+'%'

    return {'figure': figure, 'value': round(value1), 'tendency_arrow': tendency_arrow, 'tendency_value': tendency_value, 'tendency_color': tendency_color }


def hourly_drivers_model(date_range, current_date_time, current_agency='1'):
    return base_hourly_drivers_model(date_range, current_date_time, current_agency, column='drivers')

def hourly_drivers_model_alo(date_range, current_date_time, current_agency='1'):
    return base_hourly_drivers_model(date_range, current_date_time, current_agency, column='drivers_alo')    

def base_hourly_drivers_model(date_range, current_date_time, ag='1', column='drivers'):

    to_1 = datetime.strptime(current_date_time[:10], '%Y-%m-%d')
    from_1 = to_1 - timedelta(hours=int(date_range))
    to_2 = from_1
    from_2 = to_2 - timedelta(hours=int(date_range))
    df1 = au.get_hourly_drivers(au.agency[ag], from_1, to_1)
    df2 = au.get_hourly_drivers(au.agency[ag], from_2, to_2)

    value1 = df1[column].mean()
    value2 = df2[column].mean()

    trace1 = {
        'x': df1.index,
        'y': df1[column].values,
        'mode': 'lines',
        'name': 'This period',
        'line': {
            'dash': 'solid',
            'width': 2,
            'color': '#00baff'
        }
    }

    if df1.shape == df2.shape:
        df2.set_index(df1.index, inplace=True)
        df2.rename(columns = {col: f"prev_{col}" for col in df2.columns}, inplace=True)
        df = df1.merge(df2, on='date')
        df = df[[column, 'prev_' + column]]

        trace2 = {
            'x': df.index,
            'y': df['prev_' + column].values,
            'mode': 'lines',
            'name': 'Previous period',
            'line': {
                'dash': 'dot',
                'width': 2,
                'color': '#00baff'
            }
        }

        data = [trace1, trace2]

    else:
        print('Warning: current vs previous sizes are different! Probably not enought data. Use another date range.')
        data = [trace1]

    if len(df1.index) > 48:
        nticks = len(df1.index) / 24
    else:
        nticks = len(df1.index)

    layout = {
        'margin': {'b':10, 't':10},

        'xaxis': {
            'autorange': True,
            'nticks': nticks
        },
        'yaxis': {
            'autorange': True,
            'title': column
        },
        'legend': {
            'orientation': 'h',
            'xanchor': 'center',
            'y': -.3,
            'x': 0.5,
            'font': {
            'size': 14
            }
        }
    }

    figure = {'data': data, 'layout': layout}

    if value1 >= value2:
        tendency_color = 'green'        
        tendency_arrow = 'fa-long-arrow-alt-up'
    else:
        tendency_arrow = 'fa-long-arrow-alt-down'
        tendency_color = 'red'        

    tendency_value = str(abs(round(((value1/(value2+0.001))-1)*100, 2)))+'%'

    return {'figure': figure, 'value': round(value1), 'tendency_arrow': tendency_arrow, 'tendency_value': tendency_value, 'tendency_color': tendency_color }


def predict_daily_drivers_model(date_range, current_date_time, current_agency=1):
    return base_predict_daily_drivers_model(date_range, current_date_time, current_agency, column='drivers')

def predict_daily_drivers_model_alo(date_range, current_date_time, current_agency=1):
    return base_predict_daily_drivers_model(date_range, current_date_time, current_agency, column='drivers_alo')

def base_predict_daily_drivers_model(date_range, current_date_time, ag='1', column='drivers'):

    #column = 'drivers' # drivers_alo, drivers_alo_10_days
    #print(date_range, current_date_time)

    df = au.predict_daily_unique_drivers(au.agency[ag], current_date_time[:10], column=column, days=int(date_range))

    value1 = df['prediction'].mean()
    value2 = df[column].mean()

    trace_test = {
        'x': df.index,
        'y': df[column].values,
        'mode': 'lines',
        'name': 'Test Data',
        'line': {
            'dash': 'dot',
            'width': 1,
            'color': '#00baff'
        },
        'visible':'legendonly'        
    }

    trace_pred = {
        'x': df.index,
        'y': df['prediction'].values,
        'mode': 'lines',
        'name': 'Prediction',
        'line': {
            'dash': 'solid',
            'width': 2,
            'color': '#00baff'
        }
    }
    

    data = [trace_test, trace_pred]


    layout = {
        'margin': {'b':10, 't':10},    
        'xaxis': {
            'autorange': True,
            'nticks': len(df.index)
        },
        'yaxis': {
            'autorange': True,
            'title': column
        },
        'legend': {
            'orientation': 'h',
            'xanchor': 'center',
            'y': -.3,
            'x': 0.5,
            'font': {
            'size': 14
            }
        }
    }

    # if yesterday try to use another kind of figure
    if int(date_range) == 1:
        x = ['Yesterday', 'Before yesterday']
        y = [value1, value2]
        figure = go.Figure([go.Bar(x=x, y=y)])
    else:
        figure = {'data': data, 'layout': layout}

    if value1 >= value2:
        tendency_color = 'green'        
        tendency_arrow = 'fa-brain'
    else:
        tendency_arrow = 'fa-brain'
        tendency_color = 'red'        


    value = "P: {} / T: {}".format(int(round(value1)), int(round(value2)))
    value = "{}".format(int(round(value1)))

    tendency_value = str(abs(round(((value1/(value2+0.001))-1)*100, 2)))+'%'

    return {'figure': figure, 'value': value, 'tendency_arrow': tendency_arrow, 'tendency_value': tendency_value, 'tendency_color': tendency_color }


def predict_hourly_drivers_model(date_range, current_date_time, current_agency='1'):
    return base_predict_hourly_drivers_model(date_range, current_date_time, current_agency, column='drivers')

def predict_hourly_drivers_model_alo(date_range, current_date_time, current_agency='1'):
    return base_predict_hourly_drivers_model(date_range, current_date_time, current_agency, column='drivers_alo')

def base_predict_hourly_drivers_model(date_range, current_date_time, ag='1', column='drivers'):

    #column = 'drivers' # drivers_alo, drivers_alo_10_days
    #print(date_range, current_date_time)

    df = au.predict_hourly_unique_drivers(au.agency[ag], current_date_time, column=column, hours=int(date_range))

    value1 = df['prediction'].mean()
    value2 = df[column].mean()

    trace_test = {
        'x': df.index,
        'y': df[column].values,
        'mode': 'lines',
        'name': 'Test Data',
        'line': {
            'dash': 'dot',
            'width': 1,
            'color': '#00baff'
        },
        'visible':'legendonly'
    }

    trace_pred = {
        'x': df.index,
        'y': df['prediction'].values,
        'mode': 'lines',
        'name': 'Prediction',
        'line': {
            'dash': 'solid',
            'width': 2,
            'color': '#00baff'
        }
    }
    

    data = [trace_test, trace_pred]

    if len(df.index) > 24:
        nticks = len(df.index) / 2
    else:
        nticks = len(df.index)

    layout = {
        'margin': {'b':10, 't':10},    
        'xaxis': {
            'autorange': True,
            'nticks': nticks
        },
        'yaxis': {
            'autorange': True,
            'title': column
        },
        'legend': {
            'orientation': 'h',
            'xanchor': 'center',
            'y': -.3,
            'x': 0.5,
            'font': {
            'size': 14
            }
        }
    }

    figure = {'data': data, 'layout': layout}

    if value1 >= value2:
        tendency_color = 'green'        
        tendency_arrow = 'fa-brain'
    else:
        tendency_arrow = 'fa-brain'
        tendency_color = 'red'        


    value = "P: {} / T: {}".format(int(round(value1)), int(round(value2)))
    value = "{}".format(int(round(value1)))
    tendency_value = str(abs(round(((value1/(value2+0.001))-1)*100, 2)))+'%'

    return {'figure': figure, 'value': value, 'tendency_arrow': tendency_arrow, 'tendency_value': tendency_value, 'tendency_color': tendency_color }



def itineraries_model(date_range, current_date_time, current_agency='1'):
    return base_itineraries_model(date_range, current_date_time, current_agency)

def base_itineraries_model(date_range, current_date_time, ag):
    #print(date_range, current_date_time)

    column = 'itineraries'

    to_1 = datetime.strptime(current_date_time[:10], '%Y-%m-%d')
    from_1 = to_1 - timedelta(days=int(date_range))
    to_2 = from_1
    from_2 = to_2 - timedelta(days=int(date_range))
    df1 = au.get_daily_itineraries(au.agency[ag], from_1, to_1)
    df2 = au.get_daily_itineraries(au.agency[ag], from_2, to_2)

    value1 = df1[column].mean()
    value2 = df2[column].mean()

    trace1 = {
        'x': df1.index,
        'y': df1[column].values,
        'mode': 'lines',
        'name': 'This period',
        'line': {
            'dash': 'solid',
            'width': 2,
            'color': '#00baff'
        }
    }

    if df1.shape == df2.shape:
        df2.set_index(df1.index, inplace=True)
        df2.rename(columns = {col: f"prev_{col}" for col in df2.columns}, inplace=True)
        df = df1.merge(df2, on='date')
        #print(df.columns)
        df = df[[column, 'prev_' + column]]
        #print(df.shape)


        trace2 = {
            'x': df.index,
            'y': df['prev_' + column].values,
            'mode': 'lines',
            'name': 'Previous period',
            'line': {
                'dash': 'dot',
                'width': 2,
                'color': '#00baff'
            }
        }

        data = [trace1, trace2]

    else:
        print('Warning: current vs previous sizes are different! Probably not enought data. Use another date range.')
        data = [trace1]

    layout = {
        'margin': {'b':10, 't':10},    
        'xaxis': {
            'autorange': True,
            'nticks': len(df1.index)
        },
        'yaxis': {
            'autorange': True,
            'title': column
        },
        'legend': {
            'orientation': 'h',
            'xanchor': 'center',
            'y': -.3,
            'x': 0.5,
            'font': {
            'size': 14
            }
        }
    }

    # if yesterday try to use another kind of figure
    if int(date_range) == 1:
        x = ['Yesterday', 'Before yesterday']
        y = [value1, value2]
        figure = go.Figure([go.Bar(x=x, y=y)])
    else:
        figure = {'data': data, 'layout': layout}

    if value1 >= value2:
        tendency_color = 'green'        
        tendency_arrow = 'fa-long-arrow-alt-up'
    else:
        tendency_arrow = 'fa-long-arrow-alt-down'
        tendency_color = 'red'        


    tendency_value = str(abs(round(((value1/(value2+0.001))-1)*100, 2)))+'%'

    return {'figure': figure, 'value': round(value1), 'tendency_arrow': tendency_arrow, 'tendency_value': tendency_value, 'tendency_color': tendency_color }


def hourly_itineraries_model(date_range, current_date_time, ag):
    return base_hourly_itineraries_model(date_range, current_date_time, ag)

def base_hourly_itineraries_model(date_range, current_date_time, ag):
    #print(date_range, current_date_time)

    column = 'itineraries'

    to_1 = datetime.strptime(current_date_time[:10], '%Y-%m-%d')
    from_1 = to_1 - timedelta(hours=int(date_range))
    to_2 = from_1
    from_2 = to_2 - timedelta(hours=int(date_range))
    df1 = au.get_hourly_itineraries(au.agency[ag], from_1, to_1)
    df2 = au.get_hourly_itineraries(au.agency[ag], from_2, to_2)

    value1 = df1[column].mean()
    value2 = df2[column].mean()

    trace1 = {
        'x': df1.index,
        'y': df1[column].values,
        'mode': 'lines',
        'name': 'This period',
        'line': {
            'dash': 'solid',
            'width': 2,
            'color': '#00baff'
        }
    }

    if df1.shape == df2.shape:
        df2.set_index(df1.index, inplace=True)
        df2.rename(columns = {col: f"prev_{col}" for col in df2.columns}, inplace=True)
        df = df1.merge(df2, on='date')
        #print(df.columns)
        df = df[[column, 'prev_' + column]]
        #print(df.shape)


        trace2 = {
            'x': df.index,
            'y': df['prev_' + column].values,
            'mode': 'lines',
            'name': 'Previous period',
            'line': {
                'dash': 'dot',
                'width': 2,
                'color': '#00baff'
            }
        }

        data = [trace1, trace2]

    else:
        print('Warning: current vs previous sizes are different! Probably not enought data. Use another date range.')
        data = [trace1]

    if len(df1.index) > 48:
        nticks = len(df1.index) / 24
    else:
        nticks = len(df1.index)

    layout = {
        'margin': {'b':10, 't':10},    
        'xaxis': {
            'autorange': True,
            'nticks': nticks
        },
        'yaxis': {
            'autorange': True,
            'title': column
        },
        'legend': {
            'orientation': 'h',
            'xanchor': 'center',
            'y': -.3,
            'x': 0.5,
            'font': {
            'size': 14
            }
        }
    }

    # if yesterday try to use another kind of figure
    if int(date_range) == 1:
        x = ['yesterday', 'previous day']
        y = [value1, value2]
        figure = go.Figure([go.Bar(x=x, y=y)])
    else:
        figure = {'data': data, 'layout': layout}

    if value1 >= value2:
        tendency_color = 'green'        
        tendency_arrow = 'fa-long-arrow-alt-up'
    else:
        tendency_arrow = 'fa-long-arrow-alt-down'
        tendency_color = 'red'        


    tendency_value = str(abs(round(((value1/(value2+0.001))-1)*100, 2)))+'%'

    return {'figure': figure, 'value': round(value1), 'tendency_arrow': tendency_arrow, 'tendency_value': tendency_value, 'tendency_color': tendency_color }


def realtime_itineraries_model(date_range, current_date_time, ag):

    df = au.get_hourly_day_itineraries(au.agency[ag], current_date_time)
    df1 = df[['itineraries_cumsum','finished_cumsum','pending','pending_acceptance']]
    df1 = df1.fillna(0)
    column_legend = ['Created', 'Finished', 'In-progress', ' Pending acceptance']
    #'dash', 'dot', and 'dashdot'
    line_type = ['solid', 'dash', 'dot', 'dashdot']
    data = []
    colors = ['#00baff', '#00baff', '#00baff', '#00baff']
    for i, col in enumerate(df1.columns):
        data.append({
            'x': df1.index,
            'y': df1[col].values,
            'mode': 'lines',
            'name': column_legend[i],
            'line': {
                'dash': line_type[i],
                'width': 2,
                'color': colors[i]
            }
        })


    layout = {
        'margin': {'b':10, 't':10},    
        'xaxis': {
            'autorange': True,
            'nticks': len(df1.index)
        },
        'yaxis': {
            'autorange': True,
            'title': 'Itineraries'
        },
        'legend': {
            'orientation': 'h',
            'xanchor': 'center',
            'y': -.3,
            'x': 0.5,
            'font': {
            'size': 14
            }
        }
    }

    figure = {'data': data, 'layout': layout}

    if len(df1) > 0:
        value1 = '{}'.format(
            df1.loc[df1.index[-1], 'itineraries_cumsum']
            )
    else:
        value1 = ''

    if len(value1) > 0:
        tendency_color = 'green'        
        tendency_arrow = 'fa-long-arrow-alt-up-change-or-remove'
    else:
        tendency_arrow = 'fa-long-arrow-alt-down-change-or-remove'
        tendency_color = 'red'        


    tendency_value = ''

    return {'figure': figure, 'value': value1, 'tendency_arrow': tendency_arrow, 'tendency_value': tendency_value, 'tendency_color': tendency_color }

def drivers_and_itineraries_model(date_range, current_date_time, ag):

    column = 'itineraries'
    column_drivers = 'drivers_alo'

    to_1 = datetime.strptime(current_date_time[:10], '%Y-%m-%d')
    from_1 = to_1 - timedelta(days=int(date_range))
    
    df1 = au.get_daily_itineraries(au.agency[ag], from_1, to_1)
    df2 = au.get_daily_drivers(au.agency[ag], from_1, to_1)

    value1 = df1[column].mean()
    value2 = df2[column_drivers].mean()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    trace1 = {
        'x': df1.index,
        'y': df1[column].values,
        'mode': 'lines',
        'name': column,
        'line': {
            'dash': 'solid',
            'width': 2,
            'color': '#00baff'
        }
    }

    fig.add_trace(trace1, secondary_y=False)

    trace2 = {
        'x': df2.index,
        'y': df2[column_drivers].values,
        'mode': 'lines',
        'name': 'Effective Drivers',
        'line': {
            'dash': 'dashdot',
            'width': 2,
            'color': '#00baff'
        }
    }

    fig.add_trace(trace2, secondary_y=True)


    layout = {
        'margin': {'b':10, 't':10},    
        'xaxis': {
            'autorange': True,
            'nticks': len(df1.index)
        },
        'yaxis': {
            'autorange': True,
            'title': 'Itineraries'
        },
        'yaxis2': {
            'autorange': True,
            'title': 'Effective drivers'
        },

        'legend': {
            'orientation': 'h',
            'xanchor': 'center',
            'y': -.3,
            'x': 0.5,
            'font': {
            'size': 14
            }
        }
    }

    fig.update_layout(layout)    

    if int(date_range) == 1:
        x = [column, column_drivers]
        y = [value1, value2]
        figure = go.Figure([go.Bar(x=x, y=y)])
    else:
        figure = fig #{'data': data, 'layout': layout}

    if value1 >= value2:
        tendency_color = ''#'green'        
        tendency_arrow = ''#'fa-long-arrow-alt-up'
    else:
        tendency_arrow = ''#'fa-long-arrow-alt-down'
        tendency_color = ''#'red'        


    tendency_value = ''#str(abs(round(((value1/(value2+0.001))-1)*100, 2)))+'%'

    return {'figure': figure, 'value': '{:.02f}%'.format(100*(value1/value2)), 'tendency_arrow': tendency_arrow, 'tendency_value': tendency_value, 'tendency_color': tendency_color }

def occupancy_model(date_range, current_date_time, ag):

    column = 'itineraries'
    column_drivers = 'drivers_alo'

    to_1 = datetime.strptime(current_date_time[:10], '%Y-%m-%d')
    from_1 = to_1 - timedelta(days=int(date_range))
    
    df1 = au.get_daily_itineraries(au.agency[ag], from_1, to_1)
    df2 = au.get_daily_drivers(au.agency[ag], from_1, to_1)

    value1 = df1[column].mean()
    value2 = df2[column_drivers].mean()

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    trace1 = {
        'x': df1.index,
        'y': df1[column].values,
        'mode': 'lines',
        'name': column,
        'line': {
            'dash': 'dot',
            'width': 1,
            'color': '#00baff'
        }
    }

    fig.add_trace(trace1, secondary_y=False)
    #df2.set_index(df1.index, inplace=True)
    #df = df1.merge(df2, on='date')
    #df = df[[column, column_drivers]]

    trace2 = {
        'x': df2.index,
        'y': df2[column_drivers].values,
        'mode': 'lines',
        'name': 'Effective Drivers',
        'line': {
            'dash': 'dashdot',
            'width': 1,
            'color': '#00baff'
        }
    }

    fig.add_trace(trace2, secondary_y=False)

    ratio = df1[column] / df2[column_drivers]

    trace3 = {
        'x': ratio.index,
        'y': ratio.values,
        'mode': 'lines',
        'name': 'Occupancy',
        'line': {
            'dash': 'solid',
            'width': 3,
            'color': '#00baff'
        }
    }

    fig.add_trace(trace3, secondary_y=True)


    #data = [trace1, trace2]

    layout = {
        'margin': {'b':10, 't':10},    
        'xaxis': {
            'autorange': True,
            'nticks': len(df1.index)
        },
        'yaxis': {
            'autorange': True,
            'title': 'Quantity'
        },
        'yaxis2': {
            'autorange': True,
            'title': 'Occupancy (I/D)'
        },

        'legend': {
            'orientation': 'h',
            'xanchor': 'center',
            'y': -.3,
            'x': 0.5,
            'font': {
            'size': 14
            }
        }
    }
    fig.update_layout(layout)    

    if int(date_range) == 1:
        x = [column, column_drivers]
        y = [value1, value2]
        figure = go.Figure([go.Bar(x=x, y=y)])
    else:
        figure = fig #{'data': data, 'layout': layout}

    if value1 >= value2:
        tendency_color = ''#'green'        
        tendency_arrow = ''#'fa-long-arrow-alt-up'
    else:
        tendency_arrow = ''#'fa-long-arrow-alt-down'
        tendency_color = ''#'red'        


    tendency_value = ''#str(abs(round(((value1/(value2+0.001))-1)*100, 2)))+'%'

    return {'figure': figure, 'value': '{:.02f}%'.format(100*(value1/value2)), 'tendency_arrow': tendency_arrow, 'tendency_value': tendency_value, 'tendency_color': tendency_color }
