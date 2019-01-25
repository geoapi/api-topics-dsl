#! /var/www/flask/flask/bin

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/flask/')
from example import app as application
