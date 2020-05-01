import numpy as np
from ds4a.server import app
from dash.dependencies import Input, Output
import plotly.graph_objs as go

def _generate_chart(series):

    fig = go.Figure()

    # Create a trace
    trace = go.Scatter(
        y = series
    )

    layout = go.Layout(
        title="My Dash Graph",
        height=400,
        #width=1200,
        #responsize=True
    )

    data = [trace]

    fig = go.Figure(data=data, layout=layout)

    return fig


@app.callback(Output('output-data', component_property='figure'),
              [Input('input-mean', 'value'),
              Input('input-stdv', 'value'),])
def update_visualization(mean, stdv):
    time_series = np.random.normal(float(mean), float(stdv), 1000)
    chart_layout = _generate_chart(time_series)
    return chart_layout