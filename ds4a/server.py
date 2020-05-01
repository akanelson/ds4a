import dash
import dash_bootstrap_components as dbc

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    dbc.themes.BOOTSTRAP,
    'https://use.fontawesome.com/releases/v5.10.2/css/all.css'
]

# __name__ is required if we want to work with asset in local directory
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

