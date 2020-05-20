import random
from datetime import datetime
from datetime import timedelta

import plotly.graph_objects as go

# Now we can import our modulue
import practicum_utils as utils
import ds4a.models.analytics_utils as au

def user_model(date_range, current_date_time):

    column = 'drivers' # drivers_alo, drivers_alo_10_days

    print(date_range, current_date_time)

    to_1 = datetime.strptime(current_date_time[:10], '%Y-%m-%d')
    from_1 = to_1 - timedelta(days=int(date_range))
    to_2 = from_1
    from_2 = to_2 - timedelta(days=int(date_range))
    df1 = au.get_daily_drivers(au.agency['1'], from_1, to_1)
    df2 = au.get_daily_drivers(au.agency['1'], from_2, to_2)

    value1 = df1[column].mean()
    value2 = df2[column].mean()

    df2.set_index(df1.index, inplace=True)
    df2.rename(columns = {col: f"prev_{col}" for col in df2.columns}, inplace=True)
    df = df1.merge(df2, on='date')
    #print(df.columns)
    df = df[[column, 'prev_' + column]]
    print(df.shape)

    trace1 = {
        'x': df.index,
        'y': df[column].values,
        'mode': 'lines',
        'name': 'This period',
        'line': {
            'dash': 'solid',
            'width': 2,
            'color': '#00baff'
        }
    }

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

    layout = {
        'title': 'Unique {} from Agency 1'.format(column),
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
        tendency_arrow = 'up'
    else:
        tendency_arrow = 'down'
        tendency_color = 'red'        


    tendency_value = str(round(((value1/(value2+0.001))-1)*100, 2))+'%'

    return {'figure': figure, 'value': round(value1), 'tendency_arrow': tendency_arrow, 'tendency_value': tendency_value, 'tendency_color': tendency_color }


def sessions_model(date_range, current_date_time):
    return analytics_visualization_model_xxx(date_range, current_date_time)

def bounce_rate_model(date_range, current_date_time):
    return analytics_visualization_model_xxx(date_range, current_date_time)

def session_duration_model(date_range, current_date_time):
    return analytics_visualization_model_xxx(date_range, current_date_time)

def user2_model(date_range, current_date_time):
    return analytics_visualization_model_xxx(date_range, current_date_time)

def sessions2_model(date_range, current_date_time):
    return analytics_visualization_model_xxx(date_range, current_date_time)

def bounce_rate2_model(date_range, current_date_time):
    return analytics_visualization_model_xxx(date_range, current_date_time)

def analytics_visualization_model_xxx(date_range, current_date_time):
    dt_to = datetime.strptime(current_date_time[:10], '%Y-%m-%d')
    dt_from = dt_to - timedelta(days=date_range)
    
    x1_label = []
    x1 = []
    y1 = []
    for i in range(0,int(date_range)):
        x1_label.append(dt_from + timedelta(days=i))
        x1.append(i)
        y1.append(random.randint(0, 100))
    
    trace1 = {
        'x': x1_label,
        'y': y1,
        'mode': 'lines',
        'name': 'This period',
        'line': {
            'dash': 'solid',
            'width': 2,
            'color': '#00baff'
        }
    }

    x2_label = []
    x2 = []
    y2 = []
    for i in range(0,int(date_range)):
        x2_label.append(dt_from + timedelta(days=i))
        x2.append(i)
        y2.append(random.randint(0, 100))
    
    trace2 = {
        'x': x2_label,
        'y': y2,
        'mode': 'lines',
        'name': 'Previous period',
        'line': {
            'dash': 'dot',
            'width': 2,
            'color': '#00baff'
        }
    }

    data = [trace1, trace2]

    layout = {
        'title': f'From {dt_from} to {dt_to}',
        'xaxis': {
            'autorange': True,
            'nticks': date_range
        },
        'yaxis': {
            'autorange': True,
            'title': 'Drivers'
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
    
    value = random.randint(0, 100)
    
    if random.randint(0, 1) == 0:
        tendency_arrow = 'up'
    else:
        tendency_arrow = 'down'

    if random.randint(0, 1) == 0:
        tendency_color = 'red'
    else:
        tendency_color = 'green'

    tendency_value = str(round(random.random()*100, 2))+'%'

    return {'figure': figure, 'value': value, 'tendency_arrow': tendency_arrow, 'tendency_value': tendency_value, 'tendency_color': tendency_color }