import dash
import string
from math import floor
from ds4a.server import app
from dash.dependencies import Input, Output, State, MATCH, ALL    
from ds4a.models.analytics import analytics_visualization_model

    
def analytics_button_callback(instance_id, total_metrics):
    @app.callback(
        [
            Output({'type': f'dynamic-visualization-{instance_id}', 'index': ALL}, 'style'),
            Output({'type': f'dynamic-button-{instance_id}', 'index': ALL}, 'className'),
        ],
        [Input({'type': f'dynamic-button-{instance_id}', 'index': ALL}, 'n_clicks')],
        [State({'type': f'dynamic-visualization-{instance_id}', 'index': ALL}, 'id')]
    )
    def update(n_clicks, buttons):
        cols_desktop = floor(12/total_metrics)
        cols_mobile = floor(12/(total_metrics/2))
        classes = f'analytics-button-wrapper col-lg-{cols_desktop} col-md-{cols_desktop} col-sm-{cols_mobile} col-xs-{cols_mobile}'
        result_visual = []
        result_button = []
        button_clicked = dash.callback_context.triggered[0]['prop_id'].split('.')[0].replace('"',"'")[10:13]
        if button_clicked == '':
            for button in buttons:
                result_visual.append({'display': 'none'})
                result_button.append(f'{classes} analytics-button-selected-false')
            result_visual[0] = {'display': 'block'}
            result_button[0] = f'{classes} analytics-button-selected-true'
        else:
            for button in buttons:
                if button_clicked == button['index']:
                    result_visual.append({'display': 'block'})
                    result_button.append(f'{classes} analytics-button-selected-true')
                else:
                    result_visual.append({'display': 'none'})
                    result_button.append(f'{classes} analytics-button-selected-false')
        

        return [result_visual, result_button]



def analytics_range_selector_callback(instance_id):
    @app.callback(
        [
            Output({'type': f'graph-{instance_id}', 'index': ALL}, 'figure'),
            #Output({'type': f'dynamic-button-{instance_id}', 'index': ALL}, 'children'),
        ],
        [Input({'type': f'range-selector-{instance_id}', 'index': ALL}, 'value')],
        [
            State({'type': f'dynamic-visualization-{instance_id}', 'index': ALL}, 'id'),
            State('input-current-date', 'date'),
            State('input-current-hour', 'value'),
        ]
    )
    def update(date_range, range_selectors, current_date, current_hour):
        print('current date ' + current_date)
        print('current hour ' + current_hour)
        print('\n---')
        range_selected = dash.callback_context.triggered[0]['value']
        if range_selected is None:
            range_selected = 7
        result = []
        for range_selector in range_selectors:
            result.append(analytics_visualization_model(int(range_selected)+1))
        return [result]
