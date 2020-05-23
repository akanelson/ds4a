import random
from datetime import datetime
from datetime import timedelta

import plotly.graph_objects as go

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
        'title': 'Unique {} from Agency {}'.format(column, ag),
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
        }
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
        'title': 'Unique {} from Agency {}'.format(column, ag),
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
        }
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
        'title': 'Unique {} from Agency {}'.format(column, ag),
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
        'title': 'Unique {} from Agency {}'.format(column, ag),
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
