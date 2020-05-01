from ds4a.server import app
from dash.dependencies import Input, Output
from ds4a.layouts.tabs import tab_predictions, tab_historical

import plotly.graph_objs as go


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'predictions':
        return tab_predictions
    elif tab == 'historical':
        return tab_historical