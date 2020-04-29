import numpy as np
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
import time
import uuid 
from dash.dependencies import Input, Output

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




# DASH does not come with a stylesheet by default. This looks to me the more commonly used.
# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    },
    dbc.themes.BOOTSTRAP,
    'https://use.fontawesome.com/releases/v5.10.2/css/all.css'
]



# __name__ is required if we want to work with asset in local directory
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.scripts.config.serve_locally = False



LOGO_LOGGI = "/assets/loggi-logo.png"
LOGO_DS4A = "/assets/ds4a-logo.png"


header = html.Div(
    [
        html.Div(html.A(html.Img(src=LOGO_DS4A, height="50px"), href="/",), className='ds4a-logo col-lg-4 col-sm-12'),
        html.Div(html.A(html.Img(src=LOGO_LOGGI, height="50px"), href="/",), className='loggi-logo col-lg-4 col-sm-12'),
        html.Div('Last Mile Dashboard', className='dashboard-title col-lg-4 col-sm-12'),
    ],
    className='header'
)

tab_predictions =  html.Div(
    className='row',
    children = [
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*3600)+5612, label='Elapsed time', fmt='time', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-xs-12'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='Total time', fmt='time', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-xs-12'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='Total distance', fmt='{:.2f} km', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-xs-12'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='Avg. time', fmt='{:.2f} seconds', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-xs-12'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='avg work', fmt='{:.2f} avg.', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-xs-12'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='avg work', fmt='{:.2f} avg.', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-xs-12'
        ),
    ]
)

tab_historical = html.Div(
    className='row',
    children=[
        html.Div(
            create_div_carta(arr = np.random.randn(7)*(np.random.randn(1)*5)+12, label='this is it', fmt='{:.2f} %'),
            className='col-sm-4'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(7)*(np.random.randn(1)*5)+12, label='this is at', fmt='$ {:.2f}'),
            className='col-sm-4'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(7)*(np.random.randn(1)*5)+12, label='this is et', fmt='{:.2f} mm'),
            className='col-sm-4'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='elapsed time', fmt='{:.2f} km'),
            className='col-sm-4'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='total distance', fmt='{:.2f} km'),
            className='col-sm-4'
        ),
    ],
)


tabs = html.Div(
    [
        dcc.Tabs(id='tabs', value='predictions', children=[
            dcc.Tab(label='Predictions', value='predictions'),
            dcc.Tab(label='Historical', value='historical'),
        ]),
    ],
    className='tabs-selector'
)
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'predictions':
        return tab_predictions
    elif tab == 'historical':
        return tab_historical

app.layout = html.Div(
    className='container-fluid',
    children=[
        html.Div('', className='header-top'),
        header,
        html.Div('', className='header-bottom'),
        tabs,
        html.Div(id='tabs-content', className='tabs-content'),


    ]
)
app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyte