import dash_html_components as html
import dash_core_components as dcc

from ds4a.layouts.header import header
from ds4a.layouts.tabs import tabs

from ds4a.layouts.inputs import layout_inputs

main_layout = html.Div([
    
    html.Div([header], className=''),
    
    html.Div([
        html.Div([
            html.Div(
                [
                    html.H1("Controls", className='title'),
                    layout_inputs
                ], className='controls'
            ),
        ], className="col-lg-3 col-12"),
        html.Div([
            tabs
        ], className="col-lg-9 col-12"),
    ], className="row"),

    html.Div([
        html.Div([
        ], className="col-12"),
    ], className="row"),

], className="container-fluid")