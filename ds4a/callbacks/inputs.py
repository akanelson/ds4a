import dash
from ds4a.server import app
from dash.dependencies import Input, Output, State, MATCH, ALL

@app.callback(
    [
        Output({'type': f'graph-{instance_id}', 'index': ALL}, 'figure'),
        Output({'type': f'dynamic-button-value-{instance_id}', 'index': ALL}, 'children'),
        Output({'type': f'dynamic-button-tendency-arrow-{instance_id}', 'index': ALL}, 'className'),
        Output({'type': f'dynamic-button-tendency-value-{instance_id}', 'index': ALL}, 'children'),
        Output({'type': f'dynamic-button-tendency-color-{instance_id}', 'index': ALL}, 'className')

    ],
    [
        Input('input-refresh', 'n_clicks'),
    ],
    [
        State({'type': f'dynamic-visualization-{instance_id}', 'index': ALL}, 'data-model'),
        State('input-current-date', 'date'),
        State('input-current-hour', 'value')
    ]
)
def update(date_range, models, current_date, current_hour):
    return update_analytics_widget(date_range, models, current_date, current_hour)