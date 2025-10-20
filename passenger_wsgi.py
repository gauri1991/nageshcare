#!/usr/bin/env python
"""
WSGI config for cPanel deployment using Phusion Passenger.
This file is required for deploying Django on cPanel with Python apps support.
Configured for: nageshcare.com
"""

import os
import sys
from pathlib import Path

# Set the project path
project_home = '/home/wrgccpiz/public_html/nageshcare'

# Add virtual environment to Python path if it exists
# Updated for Python 3.12.11 as shown in cPanel
venv_path = '/home/wrgccpiz/virtualenv/public_html/nageshcare/3.12'
if os.path.exists(venv_path):
    # Add site-packages from virtualenv
    site_packages = os.path.join(venv_path, 'lib', 'python3.12', 'site-packages')
    if site_packages not in sys.path:
        sys.path.insert(0, site_packages)

    # Also add the bin directory for executable access
    venv_bin = os.path.join(venv_path, 'bin')
    if venv_bin not in os.environ.get('PATH', ''):
        os.environ['PATH'] = venv_bin + ':' + os.environ.get('PATH', '')

# Add project to Python path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Change to project directory
os.chdir(project_home)

# Load environment variables from .env file
# This is crucial for production deployment
env_file = os.path.join(project_home, '.env')
if os.path.exists(env_file):
    from pathlib import Path
    import re

    # Read and parse .env file
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                # Parse KEY=VALUE format
                match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$', line)
                if match:
                    key, value = match.groups()
                    # Remove quotes if present
                    value = value.strip('"\'')
                    os.environ[key] = value

# Configure PyMySQL as MySQLdb replacement (for django.db.backends.mysql)
try:
    import MySQLdb
except ImportError:
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        # If pymysql is not available, mysqlclient should be installed
        pass

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')

# Ensure DJANGO_ENV is set to production
if 'DJANGO_ENV' not in os.environ:
    os.environ['DJANGO_ENV'] = 'production'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Initialize the Django application
try:
    application = get_wsgi_application()

    # Log successful startup
    startup_log_path = os.path.join(project_home, 'logs', 'startup.log')
    os.makedirs(os.path.dirname(startup_log_path), exist_ok=True)

    import datetime
    with open(startup_log_path, 'a') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Application started successfully at: {datetime.datetime.now()}\n")
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Django settings: {os.environ.get('DJANGO_SETTINGS_MODULE')}\n")
        f.write(f"Environment: {os.environ.get('DJANGO_ENV', 'not set')}\n")

except Exception as e:
    # Log error to file for debugging
    import traceback
    import datetime

    error_log_path = os.path.join(project_home, 'logs', 'passenger_error.log')
    os.makedirs(os.path.dirname(error_log_path), exist_ok=True)

    with open(error_log_path, 'a') as f:
        f.write(f"\n\n{'='*60}\n")
        f.write(f"Error occurred at: {datetime.datetime.now()}\n")
        f.write(f"Error message: {str(e)}\n")
        f.write(f"Python path: {sys.path}\n")
        f.write(f"Environment variables:\n")
        for key in ['DJANGO_SETTINGS_MODULE', 'DJANGO_ENV', 'SECRET_KEY', 'DB_NAME']:
            value = os.environ.get(key)
            if key == 'SECRET_KEY' and value:
                value = value[:10] + '...' if len(value) > 10 else value
            f.write(f"  {key}: {value}\n")
        f.write(f"Traceback:\n")
        traceback.print_exc(file=f)
    raise
