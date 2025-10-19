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
env_loaded = False
try:
    from dotenv import load_dotenv
    env_file = os.path.join(SITE_ROOT, '.env')
    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
        env_loaded = True
except ImportError:
    # Fallback to manual parsing if python-dotenv not available
    env_file = os.path.join(SITE_ROOT, '.env')
    if os.path.exists(env_file):
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    # Parse key=value pairs
                    if '=' in line:
                        # Handle comments at end of line
                        if '#' in line:
                            # Find the first = and #
                            eq_pos = line.index('=')
                            hash_pos = line.index('#')
                            # Only strip comment if # comes after =
                            if hash_pos > eq_pos:
                                line = line[:hash_pos].strip()

                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        # Only set if not already in environment
                        if key and key not in os.environ:
                            os.environ[key] = value
            env_loaded = True
        except Exception as e:
            # Log error but continue - app might work with cPanel environment variables
            pass

# Ensure production environment (can be overridden by .env)
os.environ.setdefault('DJANGO_ENV', 'production')

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')

# Import Django application with error handling
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # If Django fails to load, create a simple error application
    import traceback
    error_message = f"Django Application Failed to Load\n\n{str(e)}\n\n{traceback.format_exc()}"

    def application(environ, start_response):
        """Fallback WSGI app that shows the error"""
        status = '500 Internal Server Error'
        response_headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, response_headers)
        return [error_message.encode('utf-8')]
