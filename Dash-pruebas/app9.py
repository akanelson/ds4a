import numpy as np
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from carta import create_div_carta

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



LOGO_LOGGI = "/assets/images/loggi-logo.png"
LOGO_CO = "/assets/images/co-logo.png"
MINI_LOGGI = "/assets/images/loggi-mini.png"
MINI_CO = "/assets/images/co-mini.png"

header = html.Div(
    [
        html.Div(html.A(html.Img(src=LOGO_LOGGI), href="/",), className='loggi-logo col-lg-4'),
        html.Div(html.A(html.Img(src=MINI_LOGGI), href="/",), className='loggi-mini col-2'),

        html.Div('Last Mile Dashboard', className='dashboard-title col-lg-4 col-sm-8 col-8'),

        html.Div(html.A(html.Img(src=LOGO_CO), href="/",), className='co-logo col-lg-4'),
        html.Div(html.A(html.Img(src=MINI_CO), href="/",), className='co-mini col-2'),

    ],
    className='header row'
)

tab_predictions =  html.Div(
    className='row',
    children = [
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*3600)+5612, label='Elapsed time', fmt='time', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-12'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='Total time', fmt='time', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-12'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='Total distance', fmt='{:.2f} km', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-12'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='Avg. time', fmt='{:.2f} seconds', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-12'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='avg work', fmt='{:.2f} avg.', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-12'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='avg work', fmt='{:.2f} avg.', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
            className='col-lg-2 col-md-4 col-sm-6 col-12'
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
app.run_server(debug=True, use_reloader=True, host='0.0.0.0')  # Turn off reloader if inside Jupyte