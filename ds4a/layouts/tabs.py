import numpy as np
import dash_html_components as html
import dash_core_components as dcc
from ds4a.components.carta import create_div_carta
from ds4a.layouts.visualization import layout_visualization


tab_predictions =  html.Div(
    [
        html.Div(
            className='row',
            children = [
                html.Div(
                    create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*3600)+5612, label='Elapsed time', fmt='time', help='Lorem ipsum dolor sit amet consectetur adipiscing elit, quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
                    className='col-lg-3 col-md-4 col-sm-6 col-6'
                ),
                html.Div(
                    create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='Total time', fmt='time', help='Lorem ipsum dolor sit amet consectetur adipiscing elit.'),
                    className='col-lg-3 col-md-4 col-sm-6 col-6'
                ),
                html.Div(
                    create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='Total distance', fmt='{:.2f} km', help='Quam blandit ante nulla vel risus, feugiat sodales fringilla eget natoque faucibus.'),
                    className='col-lg-3 col-md-4 col-sm-6 col-6'
                ),
                html.Div(
                    create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='Avg. time', fmt='{:.2f} seconds', help='Lorem ipsum dolor.'),
                    className='col-lg-3 col-md-4 col-sm-6 col-6'
                ),
                html.Div(
                    create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='avg work', fmt='{:.2f} avg.', help='Feugiat sodales fringilla eget natoque faucibus.'),
                    className='col-lg-3 col-md-4 col-sm-6 col-6'
                ),
                html.Div(
                    create_div_carta(arr = np.random.randn(30)*(np.random.randn(1)*5)+12, label='avg work', fmt='{:.2f} avg.', help='Lorem ipsum dolor sit amet.'),
                    className='col-lg-3 col-md-4 col-sm-6 col-6'
                ),
            ]
        ),
        html.Div(
            layout_visualization,
            className='row col-12'
        )
    ]
)

tab_historical = html.Div(
    className='row',
    children=[
        html.Div(
            create_div_carta(arr = np.random.randn(7)*(np.random.randn(1)*5)+12, label='this is it', fmt='{:.2f} %'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(7)*(np.random.randn(1)*5)+12, label='this is at', fmt='$ {:.2f}'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(7)*(np.random.randn(1)*5)+12, label='this is et', fmt='{:.2f} mm'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='elapsed time', fmt='{:.2f} km'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        ),
        html.Div(
            create_div_carta(arr = np.random.randn(14)*(np.random.randn(1)*5)+12, label='total distance', fmt='{:.2f} km'),
            className='col-lg-3 col-md-4 col-sm-6 col-6'
        ),
    ],
)


tabs = html.Div(
    [
        dcc.Tabs(id='tabs', value='predictions', children=[
            dcc.Tab(label='Predictions', value='predictions'),
            dcc.Tab(label='Historical', value='historical'),
        ]),
        html.Div(id='tabs-content', className='tabs-content'),
    ],
    className='tabs-selector',
)
