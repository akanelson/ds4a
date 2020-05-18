import random
from datetime import datetime
from datetime import timedelta

def user_model(date_range, current_date_time):
    return analytics_visualization_model_xxx(date_range, current_date_time)

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
    x1 = []
    y1 = []
    for i in range(0,int(date_range)):
        x1.append(i)
        y1.append(random.randint(0, 100))
    
    trace1 = {
        'x': x1,
        'y': y1,
        'mode': 'lines',
        'name': 'This period',
        'line': {
            'dash': 'solid',
            'width': 2,
            'color': '#00baff'
        }
    }

    x2 = []
    y2 = []
    for i in range(0,int(date_range)):
        x2.append(i)
        y2.append(random.randint(0, 100))
    
    trace2 = {
        'x': x2,
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


    dt_to = datetime.strptime(current_date_time, '%Y-%m-%d %H:%M:%S')
    dt_from = dt_to - timedelta(days=date_range)


    layout = {
        'title': f'From {dt_from} to {dt_to}',
        #'xaxis': {
        #    'autorange': True
        #},
        #'yaxis': {
        #    'autorange': True
        #},
        'legend': {
            'y': 0.5,
            'font': {
            'size': 14
            }
        }
    }

    return {'data': data, 'layout': layout}