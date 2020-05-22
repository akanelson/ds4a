import dash
from ds4a.server import app
from dash.dependencies import Input, Output, State, MATCH, ALL

@app.callback(
    [
        Output({'generic-type': 'range-selector', 'type': ALL, 'index': ALL}, 'value'),
    ],
    [
        Input('input-refresh', 'n_clicks'),
    ],
    [
        State({'index': ALL, 'type': ALL, 'generic-type': 'range-selector'}, 'value')
    ]
)
def update(n_clicks, range_selectors):
    result_range = []
    for range_selector in range_selectors:
        # Force refreshing all range selectors with the current value, which will force refreshing all values and figures.
        result_range.append(range_selector)
    return [result_range]
