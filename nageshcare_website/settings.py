"""
Django settings for nageshcare_website project.

This file imports settings based on the DJANGO_ENV environment variable.
- Development: uses settings_dev.py
- Production: uses settings_prod.py (default for safety)

To switch environments, set DJANGO_ENV environment variable:
    export DJANGO_ENV=development # For development
    export DJANGO_ENV=production  # For production (default)
"""

import os

# Determine which settings to use based on environment
# Default to production for safety - development must be explicitly set
DJANGO_ENV = os.environ.get('DJANGO_ENV', 'production')

if DJANGO_ENV == 'development':
    from .settings_dev import *
else:
    # Use production settings as default
    from .settings_prod import *
