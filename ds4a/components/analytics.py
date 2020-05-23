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

    if 'help' in metric:
        help = metric['help']
    else:
        help = 'No description provided'
        
    return  html.Div(
        html.Div(
            html.Div(
                [
                    
                    html.Div(
                        [
                            html.I(className="fas fa-question-circle fa-lg"),
                            html.Span(help, className='tooltip-text'),
                        ],
                        className='tooltip-wrapper'
                    ),
                    html.Div(metric['label'], className="analytics-metric-label"),
                    html.Div(model['value'], className="analytics-metric-value", id={'index': f'{button_id}', 'type': f'dynamic-button-value-{instance_id}', 'generic-type': 'dynamic-button-value'}),
                    html.Div(
                        [
                            html.I(' ', className=f"analytics-icon fas {model['tendency_arrow']}", id={'index': f'{button_id}', 'type': f'dynamic-button-tendency-arrow-{instance_id}', 'generic-type': 'dynamic-button-tendency-arrow'}),
                            html.Span(model['tendency_value'], id={'index': f'{button_id}', 'type': f'dynamic-button-tendency-value-{instance_id}', 'generic-type': 'dynamic-button-tendency-value'})
                        ],
                        className=f"analytics-metric-tendency analytics-metric-tendency-color-{model['tendency_color']}",
                        id={'index': f'{button_id}', 'type': f'dynamic-button-tendency-color-{instance_id}', 'generic-type': 'dynamic-button-tendency-color'}
                    ),
                ],
                className="analytics-metric-button"
            ),
            className="analytics-button-container"
        ),
        className=f"analytics-button-wrapper col-lg-{cols_desktop} col-md-{cols_desktop} col-sm-{cols_mobile} col-xs-{cols_mobile} analytics-button-selected-{metric['selected']}",
        id={'index': f'{button_id}', 'type': f'dynamic-button-{instance_id}', 'generic-type': 'dynamic-button'}
        
    )

def analytics_visualization(model, metric, visual_id, instance_id):

    return  html.Div(
                [
                    dcc.Graph(id={'index': f'{visual_id}', 'type': f'graph-{instance_id}', 'generic-type': 'dynamic-graph'}, figure=model['figure']) 
                ],
                style={'display': 'none'},
                className="analytics-visualization-wrapper col",
                id={'index': f'{visual_id}', 'type': f'dynamic-visualization-{instance_id}', 'generic-type': 'dynamic-visualization'},
                **{'data-model': metric['model']}
    )

def analytics_range_selector(instance_id, range_selector):
    
    options = []
    for key, value in range_selector.items():
        options.append({'label': key, 'value': value})

    output = dcc.Dropdown(
        id={'index': '1', 'type': f'range-selector-{instance_id}', 'generic-type': 'range-selector'},
        options = options,
        value = options[0]['value'],
        clearable=False,
        className="analytics-range-selector-wrapper col",

    )
    return output

def analitycs(widget):
    instance_id = randomString(2)

    metrics, config = widget

    #get the first value on the key, value pair to initialize the range selector
    initial_range_selector_value = next(iter(config['range_selector'].items()))[1]

    #print('\n----- begin range selector ----')
    #print(config['range_selector'])
    #print('first data '+str(       ))
    #print('\n----- end range selector ----')    

    buttons = html.Div([], className="row analytics-button-row")
    visualizations = html.Div([], className="row analytics-visualization-row")
    if config['range_selector'] is not None:
        range_selector = html.Div(analytics_range_selector(instance_id, config['range_selector']), className="row analytics-range-selector-row")
    else:
        range_selector = ''

    for metric in metrics:
        # First time initialization call
        function_model = getattr(ds4a.models.analytics, metric['model'])
        this_model = function_model(initial_range_selector_value, '2020-02-03', '1')
        
        local_id = randomString(3)
        
        buttons.children.append(analytics_button(this_model, metric, len(metrics), local_id, instance_id))
        visualizations.children.append(analytics_visualization(this_model, metric, local_id, instance_id))
    
    analytics_button_callback(instance_id, len(metrics))
    analytics_range_selector_callback(instance_id)

    markup = dcc.Loading(
        [   
            html.Div(
                    [
                        html.H1(config['title'], className='analytics-title'),
                        buttons,
                        visualizations,
                        range_selector,
                    ],
                    className="analytics-wrapper"
            )
        ], id='loading-'+instance_id, className='analytics-loading')
    return markup
