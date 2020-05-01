import dash_html_components as html
import dash_core_components as dcc

layout_visualization = html.Div([
    html.H3("Visualization"),
    dcc.Graph(id='output-data')
])