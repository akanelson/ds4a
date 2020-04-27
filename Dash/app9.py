import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import time

def create_div_carta(arr, label='', fmt='{:.2f}', classname='three columns'):
    """Create a carta component (DIV) using the last value of the array"""
    """(arr[-1]) and creating a line with the array values at arr"""

    USE_MARKERS = False

    n = len(arr)

    # Create figure line
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.linspace(0, 1, n), y=arr,
        mode='lines+markers' if USE_MARKERS else 'lines',
        line=dict(color='lightblue', width=2),
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

    if fmt == 'time':
        unit = time.strftime('%H:%M:%S', time.gmtime(int(arr[-1])))
    else:
        unit = fmt.format(arr[-1])

    # return CARTA DIV component
    return html.Div(
        className = 'wx_carta ',
        children =[
            html.Span(label),
    		html.H3(unit),
    		dcc.Graph(figure=fig, config={'displayModeBar': False})
    	],
	)

# DASH does not come with a stylesheet by default. This looks to me the more commonly used.
# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

# __name__ is required if we want to work with asset in local directory
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.scripts.config.serve_locally = False
 
app.layout = html.Div(
    className='container',
    children=[
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='twelve columns',
                    children=html.H1('Title'),
                    style={'textAlign': 'center', 'backgroundColor': '#f6f6f6'}                
                )
            ]
        ),
        html.Div(
        	className='row',
            children = [
                html.Div(
                    className = '',
                    children = [
                        html.Div(
        	    	       children=[
                                create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*3600)+5612, label='Elapsed time', fmt='time'),
                                create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='Total time', fmt='time'),
                                create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='Total distance', fmt='{:.2f} km'),
                                create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='Avg. time', fmt='{:.2f} seconds'),
                                create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='avg time',fmt='{:.2f} seconds'),
                                create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='avg work', fmt='{:.2f} avg.')
                            ]
                        )
                    ],
                ),
            ]
        ),
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='',
                    children = [
                        html.Div(
                           children=[
                                create_div_carta(arr = np.random.randn(7)*(np.random.randn(1)*5)+12, label='this is it', fmt='{:.2f} %'),
                                create_div_carta(arr = np.random.randn(7)*(np.random.randn(1)*5)+12, label='this is at', fmt='$ {:.2f}'),
                                create_div_carta(arr = np.random.randn(7)*(np.random.randn(1)*5)+12, label='this is et', fmt='{:.2f} mm'),
                                create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='elapsed time', fmt='{:.2f} km'),
                                create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='total time', fmt='{:.2f} km'),
                                create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='total distance', fmt='{:.2f} km'),
                            ]
                        )
                    ],
                ),
            ],
        )        
    ]
)
app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyte