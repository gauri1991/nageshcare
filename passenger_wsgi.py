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

# Load environment variables from .env file FIRST (before setting defaults)
# This uses python-dotenv for proper .env parsing
try:
    from dotenv import load_dotenv
    env_file = os.path.join(SITE_ROOT, '.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
except ImportError:
    # Fallback to manual parsing if python-dotenv not available
    env_file = os.path.join(SITE_ROOT, '.env')
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip().strip('"').strip("'")
                    os.environ.setdefault(key.strip(), value)

# Ensure production environment (can be overridden by .env)
os.environ.setdefault('DJANGO_ENV', 'production')

# Configure PyMySQL to act as MySQLdb replacement
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
