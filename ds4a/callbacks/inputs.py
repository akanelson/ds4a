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



@app.callback(
    [
        Output('historical', 'active'),
        Output('real_time', 'active'),
        Output('prediction', 'active'),
        Output({'wrapper_type': ALL, 'instance': ALL}, 'style')
    ],
    [
        Input('historical', 'n_clicks'),
        Input('real_time', 'n_clicks'),
        Input('prediction', 'n_clicks'),
    ],
    [
        State({'wrapper_type': ALL, 'instance': ALL}, 'id')
    ]
)
def update(menu_historical, menu_real_time, menu_prediction, wrappers):
    result_wrappers = []
    
    if dash.callback_context.triggered[0]['prop_id'].split('.')[0] == '':
        menu_clicked = 'real_time'
    else:
        menu_clicked = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    for wrapper in wrappers:
        if menu_clicked == wrapper['wrapper_type']:
            result_wrappers.append({'display': 'block'})
        else:
            result_wrappers.append({'display': 'none'})
    if menu_clicked == 'historical':
        return [True, False, False, result_wrappers]
    elif menu_clicked == 'real_time':
        return [False, True, False, result_wrappers]
    elif menu_clicked == 'prediction':
        return [False, False, True, result_wrappers]
    else:
        return [False, True, False, result_wrappers]

    