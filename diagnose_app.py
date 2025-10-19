#!/usr/bin/env python3
"""
Diagnostic script for cPanel Django deployment.
Run this on your server to check configuration and dependencies.
"""

import sys
import os

print("=" * 80)
print("DJANGO APP DIAGNOSTIC TOOL")
print("=" * 80)
print()

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"Script location: {BASE_DIR}")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print()

# Check if virtual environment is activated
print("-" * 80)
print("VIRTUAL ENVIRONMENT CHECK")
print("-" * 80)
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("✓ Virtual environment is activated")
    print(f"  Virtual env: {sys.prefix}")
else:
    print("✗ Virtual environment NOT activated")
    print("  Run: source /home/wrgccpiz/virtualenv/public_html/nageshcare/3.12/bin/activate")
print()

# Check required files
print("-" * 80)
print("REQUIRED FILES CHECK")
print("-" * 80)
required_files = [
    'manage.py',
    'passenger_wsgi.py',
    '.env',
    'requirements.txt',
    'nageshcare_website/settings.py',
]

for file in required_files:
    file_path = os.path.join(BASE_DIR, file)
    exists = os.path.exists(file_path)
    status = "✓" if exists else "✗"
    print(f"{status} {file}: {'exists' if exists else 'MISSING'}")
print()

# Check required Python packages
print("-" * 80)
print("PYTHON PACKAGES CHECK")
print("-" * 80)
required_packages = {
    'django': 'Django',
    'pymysql': 'PyMySQL',
    'dotenv': 'python-dotenv',
    'PIL': 'Pillow',
    'crispy_forms': 'django-crispy-forms',
}

for module, package in required_packages.items():
    try:
        __import__(module)
        print(f"✓ {package} installed")
    except ImportError:
        print(f"✗ {package} NOT installed - run: pip install {package}")
print()

# Try loading environment variables
print("-" * 80)
print("ENVIRONMENT VARIABLES CHECK")
print("-" * 80)
env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    print(f"✓ .env file exists ({os.path.getsize(env_file)} bytes)")

    # Try loading with dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print("✓ Loaded .env with python-dotenv")
    except ImportError:
        print("⚠ python-dotenv not available, using fallback")

    # Check critical variables
    critical_vars = [
        'DJANGO_ENV',
        'SECRET_KEY',
        'ALLOWED_HOSTS',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
    ]

    print("\nCritical environment variables:")
    for var in critical_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            if 'PASSWORD' in var or 'SECRET' in var:
                display = value[:5] + "..." if len(value) > 5 else "***"
            else:
                display = value
            print(f"  ✓ {var} = {display}")
        else:
            print(f"  ✗ {var} = NOT SET")
else:
    print("✗ .env file NOT found")
print()

# Try importing Django and checking configuration
print("-" * 80)
print("DJANGO CONFIGURATION CHECK")
print("-" * 80)

# Add project to path
sys.path.insert(0, BASE_DIR)

# Configure PyMySQL before Django
try:
    import pymysql
    pymysql.install_as_MySQLdb()
    print("✓ PyMySQL configured as MySQLdb")
except ImportError:
    print("✗ PyMySQL not available")

try:
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')

    # Try importing Django
    import django
    print(f"✓ Django imported (version {django.get_version()})")

    # Try setting up Django
    django.setup()
    print("✓ Django setup successful")

    # Check settings
    from django.conf import settings
    print(f"✓ Settings loaded")
    print(f"  DEBUG = {settings.DEBUG}")
    print(f"  ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
    print(f"  DATABASE ENGINE = {settings.DATABASES['default']['ENGINE']}")
    print(f"  DATABASE NAME = {settings.DATABASES['default']['NAME']}")

except Exception as e:
    print(f"✗ Django setup failed: {e}")
    import traceback
    traceback.print_exc()
print()

# Try database connection
print("-" * 80)
print("DATABASE CONNECTION CHECK")
print("-" * 80)
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
    print("✓ Database connection successful")
    print(f"  MySQL version: {connection.mysql_version}")
except Exception as e:
    print(f"✗ Database connection failed: {e}")
print()

# Check file permissions
print("-" * 80)
print("FILE PERMISSIONS CHECK")
print("-" * 80)
critical_paths = [
    BASE_DIR,
    os.path.join(BASE_DIR, 'passenger_wsgi.py'),
    os.path.join(BASE_DIR, 'manage.py'),
    os.path.join(BASE_DIR, 'logs'),
    os.path.join(BASE_DIR, 'media'),
    os.path.join(BASE_DIR, 'staticfiles'),
]

for path in critical_paths:
    if os.path.exists(path):
        perms = oct(os.stat(path).st_mode)[-3:]
        print(f"  {path}: {perms}")
    else:
        print(f"  {path}: NOT FOUND (may need to be created)")
print()

print("=" * 80)
print("DIAGNOSTIC COMPLETE")
print("=" * 80)
print()
print("If you see errors above, fix them and run this script again.")
print("After all checks pass, restart your Python app in cPanel.")
