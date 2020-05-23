import numpy as np
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go
import random
import time

def create_div_carta(arr, label='', fmt='{:.2f}', help='No info'):
    """Create a carta component (DIV) using the last value of the array"""
    """(arr[-1]) and creating a line with the array values at arr"""

    USE_MARKERS = False

    n = len(arr)

    # Create figure line
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.linspace(0, 1, n), y=arr,
        mode='lines+markers' if USE_MARKERS else 'lines',
        line=dict(color='#00baff', width=2),
        fill='tozeroy',
        hoverinfo='none',
        ))
    # Define layout where line is shown
    fig.update_layout(
        autosize=True,
        height=30,
        yaxis=dict(ticktext=[], tickvals=[]),
        xaxis=dict(ticktext=[], tickvals=[]),
        margin=dict(l=5, r=5, b=5, t=5),
        plot_bgcolor='#ffffff',
        paper_bgcolor="#ffffff",
    )

    # Build value and apply format
    if fmt == 'time':
        value = time.strftime('%H:%M:%S', time.gmtime(int(arr[-1])))
    else:
        value = fmt.format(arr[-1])

    # return CARTA DIV component
    return html.Div(
        className = 'wx_carta ',
        children =[
            html.Div(
                [
                    html.I(className="fas fa-question-circle fa-lg"),
                    html.Span(help, className='tooltip-text'),
                ],
                className='tooltip-wrapper'
            ),
            html.Span(label, className='label'),
    		html.H3(value, className='value'),
    		dcc.Graph(figure=fig, config={'displayModeBar': False}, className='sparkline'),
    	],
	)

def realtime_cartas(current_date=None, current_time=None, current_agency=None):
    cartas = html.Div([
        
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*3600)+5612, label='Elapsed time', fmt='time', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='Total time', fmt='time', help='Lorem ipsum dolor sit amet consectetur adipiscing elit.'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='Total distance', fmt='{:.2f} km', help='Quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='Avg. time', fmt='{:.2f} seconds', help='Lorem ipsum dolor.'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        )
    ], className='row')
    
    return cartas
    