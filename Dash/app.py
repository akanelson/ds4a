import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import plotly.express as px
from dash.dependencies import Input, Output


import practicum_utils as utils
from practicum_utils import get_loggi_files, global_connect, run_query, explained_time, careful_query
db = global_connect()
df = careful_query("""
SELECT DATE(created), COUNT(1) as cant,
        SUM(CASE WHEN status = 'finished' THEN 1 ELSE 0	END) as s_finished,
        SUM(CASE WHEN status != 'finished' THEN 1 ELSE 0 END) as s_notfinished,
        SUM(CASE WHEN status = 'dropped' THEN 1 ELSE 0 END) as s_dropped
FROM ITINERARIES
GROUP BY DATE(created)
ORDER BY DATE(created)
""")
#fig = px.histogram(df.s_finished)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    dcc.RadioItems(
        id='type',
        options=[
            {'label': 'Finished', 'value': 's_finished'},
            {'label': 'Not Finished', 'value': 's_notfinished'},
            {'label': 'Dropped', 'value': 's_dropped'}
        ],
        value='s_finished'
    ),    

    dcc.Graph(
        id='loggi'
    ),

    dcc.Graph(
        id='itineraries',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),


    html.Div([
        html.Label('Dropdown'),
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='MTL'
        ),

        html.Label('Multi-Select Dropdown'),
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value=['MTL', 'SF'],
            multi=True
        ),

        html.Label('Radio Items'),
        dcc.RadioItems(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='MTL'
        ),

        html.Label('Checkboxes'),
        dcc.Checklist(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value=['MTL', 'SF']
        ),

        html.Label('Text Input'),
        dcc.Input(value='MTL', type='text'),

        html.Label('Slider'),
        dcc.Slider(
            min=0,
            max=9,
            marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
            value=5,
        ),
    ], style={'columnCount': 3})
],)

@app.callback(
    Output('loggi', 'figure'),
    [Input(component_id='type', component_property='value')]
)
def cualquier_cosa_que_este_debajo(input_value):    
    return px.scatter(df, x="s_finished", y=input_value)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
