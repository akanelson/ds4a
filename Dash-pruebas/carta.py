import numpy as np
import time
import uuid
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go


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

    # Generate dinamic component ID
    component_id = 'target-'+str(uuid.uuid1())

    # return CARTA DIV component
    return html.Div(
        className = 'wx_carta ',
        children =[
            html.Div(
                [
                    html.I(className="fas fa-question-circle fa-lg", id=component_id),
                    dbc.Tooltip(help, target=component_id, placement='left', innerClassName='help', arrowClassName='help-arrow'),
                ],
                className='tooltip-wrapper'
            ),
            html.Span(label, className='label'),
    		html.H3(value, className='value'),
    		dcc.Graph(figure=fig, config={'displayModeBar': False}, className='sparkline')
    	],
	)