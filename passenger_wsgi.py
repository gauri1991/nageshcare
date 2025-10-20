#!/usr/bin/env python
"""
WSGI config for cPanel deployment using Phusion Passenger.
Simplified version - lets cPanel handle virtualenv and environment setup.
Configured for: nageshcare.com
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

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')

# Ensure DJANGO_ENV is set to production
os.environ.setdefault('DJANGO_ENV', 'production')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Initialize the Django application
application = get_wsgi_application()
