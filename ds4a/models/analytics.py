import random

def analytics_visualization_model(date_range):
    x1 = []
    y1 = []
    for i in range(1,int(date_range)):
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
    for i in range(1,int(date_range)):
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

    layout = {
        'title': 'Line Dash',
        'xaxis': {
            'autorange': True
        },
        'yaxis': {
            'autorange': True
        },
        'legend': {
            'y': 0.5,
            'traceorder': 'reversed',
            'font': {
            'size': 16
            }
        }
    }

    return {'data': data, 'layout': layout}