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