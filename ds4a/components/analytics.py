import dash_html_components as html
import dash_core_components as dcc
from ds4a.callbacks.analytics import *
from math import floor
import random
import string
import ds4a.models.analytics


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def analytics_button(model, metric, cols, button_id, instance_id):
    cols_desktop = floor(12/cols)
    cols_mobile = floor(12/(cols/2))
    return  html.Div(
        html.Div(
            html.Div(
                [
                    html.Div(metric['label'], className="analytics-metric-label"),
                    html.Div(model['value'], className="analytics-metric-value", id={'index': f'{button_id}', 'type': f'dynamic-button-value-{instance_id}'}),
                    html.Div(
                        [
                            html.I(' ', className=f"analytics-icon fas fa-long-arrow-alt-{model['tendency_arrow']}", id={'index': f'{button_id}', 'type': f'dynamic-button-tendency-arrow-{instance_id}'}),
                            html.Span(model['tendency_value'], id={'index': f'{button_id}', 'type': f'dynamic-button-tendency-value-{instance_id}'})
                        ],
                        className=f"analytics-metric-tendency analytics-metric-tendency-color-{model['tendency_color']}",
                        id={'index': f'{button_id}', 'type': f'dynamic-button-tendency-color-{instance_id}'}
                    ),
                ],
                className="analytics-metric-button"
            ),
            className="analytics-button-container"
        ),
        className=f"analytics-button-wrapper col-lg-{cols_desktop} col-md-{cols_desktop} col-sm-{cols_mobile} col-xs-{cols_mobile} analytics-button-selected-{metric['selected']}",
        id={'index': f'{button_id}', 'type': f'dynamic-button-{instance_id}'}
        
    )

def analytics_visualization(model, metric, visual_id, instance_id):

    return  html.Div(
                [
                    dcc.Graph(id={'index': f'{visual_id}', 'type': f'graph-{instance_id}'}, figure=model['figure']) 
                ],
                style={'display': 'none'},
                className="analytics-visualization-wrapper col",
                id={'index': f'{visual_id}', 'type': f'dynamic-visualization-{instance_id}'},
                **{'data-model': metric['model']}
    )

def analytics_range_selector(instance_id):
    output = dcc.Dropdown(
        id={'index': '', 'type': f'range-selector-{instance_id}'},
        options = [
            {'label': 'Yesterday', 'value': '1'},
            {'label': 'Last Week', 'value': '7'},
            {'label': 'Last 2 Weeks', 'value': '14'},
            {'label': 'Last Month', 'value': '30'},
        ],
        value = '7',
        clearable=False,
        className="analytics-range-selector-wrapper col",

    )
    return output

def analitycs(metrics):
    instance_id = randomString(2)

    buttons = html.Div([], className="row analytics-button-row")
    visualizations = html.Div([], className="row analytics-visualization-row")
    range_selector = html.Div(analytics_range_selector(instance_id), className="row analytics-range-selector-row")

    for metric in metrics:
        # First time initialization call
        function_model = getattr(ds4a.models.analytics, metric['model'])
        this_model = function_model(7, '2019-11-12')
        
        local_id = randomString(3)
        
        buttons.children.append(analytics_button(this_model, metric, len(metrics), local_id, instance_id))
        visualizations.children.append(analytics_visualization(this_model, metric, local_id, instance_id))
    
    analytics_button_callback(instance_id, len(metrics))
    analytics_range_selector_callback(instance_id)

    markup = dcc.Loading(
        [   
            html.Div(
                    [
                        buttons,
                        visualizations,
                        range_selector,
                    ],
                    className="analytics-wrapper"
            )
        ], id='loading-'+instance_id)
    return markup
