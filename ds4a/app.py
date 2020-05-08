import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ds4a.server import app
from ds4a.layouts.main import main_layout

# Include layout
app.layout = main_layout

# Include callbacks (Needs to be assigned after setting layout up)
from ds4a.callbacks.main import *

# Inititalize server variable due to it is needed for Flask to run in Apache
server = app

# Initializing app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8050')
