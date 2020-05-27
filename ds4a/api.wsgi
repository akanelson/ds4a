#! /usr/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)

# Set the location where the working directory is
sys.path.insert(0, '/var/www/practicum/ds4a/')
from api import app
# Initialize application variable with the app.server from the app.py
application = app