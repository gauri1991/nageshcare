"""
Django settings for nageshcare_website project.

This file imports settings based on the DJANGO_ENV environment variable.
- Development: uses settings_dev.py (default)
- Production: uses settings_prod.py

To switch environments, set DJANGO_ENV environment variable:
    export DJANGO_ENV=production  # For production
    export DJANGO_ENV=development # For development (default)
"""

import os

# Determine which settings to use based on environment
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
    from .settings_prod import *
else:
    from .settings_dev import *
