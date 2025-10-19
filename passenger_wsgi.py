"""
Passenger WSGI file for cPanel Python App deployment.

This file is used by cPanel's Python App to run your Django application.
Place this file in the root of your application directory on cPanel.
"""

import os
import sys

# Add your project directory to the sys.path
# IMPORTANT: Update this path to match your cPanel directory structure
# Example: /home/username/nageshcare
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SITE_ROOT)

# Set environment to production
os.environ['DJANGO_ENV'] = 'production'

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')

# Load environment variables from .env file if it exists
env_file = os.path.join(SITE_ROOT, '.env')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key, value)

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
