import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Add directory where we have our configuration
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + '/..')) + '/initial_exploratory_analysis/')

# Now we can import our modulue
import practicum_utils as utils

# db connect
db = utils.global_connect()

from ds4a.server import app
from ds4a.layouts.main import main_layout

# Suppres callback expceptions
app.config['suppress_callback_exceptions']=True

# Include layout
app.title = 'Planify App'
app.layout = main_layout

# Include callbacks (Needs to be assigned after setting layout up)
from ds4a.callbacks.main import *

# Inititalize server variable due to it is needed for Flask to run in Apache
server = app

# Initializing app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8050')
