#!/usr/bin/env python
"""
WSGI config for cPanel deployment using Phusion Passenger.
This file is required for deploying Django on cPanel with Python apps support.
"""

import os
import sys

# Set the project path
project_home = '/home/wrgccpiz/public_html/nageshcare'

# Add project to Python path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Change to project directory
os.chdir(project_home)

# Configure PyMySQL as MySQLdb replacement (for django.db.backends.mysql)
try:
    import MySQLdb
except ImportError:
    import pymysql
    pymysql.install_as_MySQLdb()

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
