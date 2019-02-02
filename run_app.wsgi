#!/usr/bin/python
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/flask/')
from __init__  import app as application
