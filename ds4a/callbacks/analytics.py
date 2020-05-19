import dash
import string
from math import floor
from ds4a.server import app
from dash.dependencies import Input, Output, State, MATCH, ALL    
import ds4a.models.analytics
import random
import copy

    
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
            Output({'type': f'dynamic-button-value-{instance_id}', 'index': ALL}, 'children'),
            Output({'type': f'dynamic-button-tendency-arrow-{instance_id}', 'index': ALL}, 'className'),
            Output({'type': f'dynamic-button-tendency-value-{instance_id}', 'index': ALL}, 'children'),
            Output({'type': f'dynamic-button-tendency-color-{instance_id}', 'index': ALL}, 'className')

        ],
        [Input({'type': f'range-selector-{instance_id}', 'index': ALL}, 'value')],
        [
            State({'type': f'dynamic-visualization-{instance_id}', 'index': ALL}, 'data-model'),
            State('input-current-date', 'date'),
            State('input-current-hour', 'value')
        ]
    )
    def update(date_range, models, current_date, current_hour):
        current_date_time = current_date.split(' ')[0] + ' ' + current_hour
        range_selected = dash.callback_context.triggered[0]['value']
        if range_selected is None:
            range_selected = 7
        graphs = []
        values = []
        tendency_arrows = []
        tendency_values = []
        tendency_colors = []
        for model in models:
            function_model = getattr(ds4a.models.analytics, model)
            this_model = function_model(int(range_selected), current_date_time)
            graphs.append(this_model['figure'])
            values.append(this_model['value'])
            tendency_arrows.append("analytics-icon fas fa-long-arrow-alt-"+this_model['tendency_arrow'])
            tendency_values.append(this_model['tendency_value'])
            tendency_colors.append("analytics-metric-tendency analytics-metric-tendency-color-"+this_model['tendency_color'])
        
        return [graphs, values, tendency_arrows, tendency_values, tendency_colors]
