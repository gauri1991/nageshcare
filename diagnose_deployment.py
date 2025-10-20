#!/usr/bin/env python3
"""
NageshCare Deployment Diagnostic Script
Run this script on the server to diagnose deployment issues
Usage: python diagnose_deployment.py
"""

import os
import sys
from pathlib import Path

print("=" * 80)
print("NAGESHCARE DEPLOYMENT DIAGNOSTICS")
print("=" * 80)
print()

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent
print(f"✓ Base Directory: {BASE_DIR}")
print()

# ============================================================================
# 1. CHECK PYTHON VERSION AND PATH
# ============================================================================
print("1. PYTHON VERSION & PATH")
print("-" * 80)
print(f"   Python Version: {sys.version}")
print(f"   Python Executable: {sys.executable}")
print(f"   Virtual Environment: {'Yes' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'No'}")
print()

# ============================================================================
# 2. CHECK ENVIRONMENT FILE
# ============================================================================
print("2. ENVIRONMENT FILE (.env)")
print("-" * 80)
env_file = BASE_DIR / '.env'
if env_file.exists():
    print(f"   ✓ .env file exists: {env_file}")

    # Check permissions
    import stat
    perms = oct(os.stat(env_file).st_mode)[-3:]
    print(f"   ✓ Permissions: {perms}")

    # Check if readable
    try:
        with open(env_file, 'r') as f:
            lines = f.readlines()
        print(f"   ✓ File is readable ({len(lines)} lines)")

        # Parse and check key variables (without showing sensitive values)
        env_vars = {}
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _ = line.split('=', 1)
                env_vars[key.strip()] = True

        required_vars = ['SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS', 'DB_ENGINE',
                        'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST']

        print(f"\n   Required Variables Check:")
        for var in required_vars:
            status = "✓" if var in env_vars else "✗"
            print(f"      {status} {var}")

    except Exception as e:
        print(f"   ✗ Error reading file: {e}")
else:
    print(f"   ✗ .env file NOT FOUND at {env_file}")
print()

# ============================================================================
# 3. CHECK DJANGO IMPORTS
# ============================================================================
print("3. DJANGO IMPORTS")
print("-" * 80)
try:
    import django
    print(f"   ✓ Django imported successfully")
    print(f"   ✓ Django version: {django.get_version()}")
except ImportError as e:
    print(f"   ✗ Django import failed: {e}")
    sys.exit(1)
print()

# ============================================================================
# 4. CHECK CRITICAL DEPENDENCIES
# ============================================================================
print("4. CRITICAL DEPENDENCIES")
print("-" * 80)
dependencies = {
    'django': 'Django',
    'pymysql': 'PyMySQL (Database)',
    'PIL': 'Pillow (Images)',
    'whitenoise': 'WhiteNoise (Static Files)',
    'crispy_forms': 'Django Crispy Forms',
    'dotenv': 'Python Dotenv',
}

for module, name in dependencies.items():
    try:
        __import__(module)
        print(f"   ✓ {name}")
    except ImportError:
        print(f"   ✗ {name} - NOT INSTALLED")
print()

# ============================================================================
# 5. LOAD ENVIRONMENT VARIABLES
# ============================================================================
print("5. LOADING ENVIRONMENT VARIABLES")
print("-" * 80)
try:
    from dotenv import load_dotenv

    # Try to load .env
    env_loaded = load_dotenv(env_file)
    print(f"   {'✓' if env_loaded else '✗'} load_dotenv() result: {env_loaded}")

    # Check if variables are accessible
    test_vars = ['DJANGO_ENV', 'SECRET_KEY', 'DEBUG', 'DB_NAME', 'DB_USER', 'DB_HOST']
    print(f"\n   Environment Variables Loaded:")
    for var in test_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            if var in ['SECRET_KEY', 'DB_PASSWORD']:
                display_value = value[:5] + '***' if len(value) > 5 else '***'
            else:
                display_value = value
            print(f"      ✓ {var} = {display_value}")
        else:
            print(f"      ✗ {var} = NOT SET")

except Exception as e:
    print(f"   ✗ Error loading environment: {e}")
print()

# ============================================================================
# 6. DJANGO SETTINGS IMPORT
# ============================================================================
print("6. DJANGO SETTINGS")
print("-" * 80)
try:
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')

    import django
    django.setup()

    print(f"   ✓ Django setup successful")

    from django.conf import settings
    print(f"   ✓ Settings module: {settings.SETTINGS_MODULE}")
    print(f"   ✓ DEBUG mode: {settings.DEBUG}")
    print(f"   ✓ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"   ✓ Database ENGINE: {settings.DATABASES['default']['ENGINE']}")
    print(f"   ✓ Database NAME: {settings.DATABASES['default']['NAME']}")
    print(f"   ✓ Database HOST: {settings.DATABASES['default']['HOST']}")

except Exception as e:
    print(f"   ✗ Django settings error: {e}")
    import traceback
    print(f"\n   Traceback:")
    print("   " + "\n   ".join(traceback.format_exc().split("\n")))
    sys.exit(1)
print()

# ============================================================================
# 7. DATABASE CONNECTION TEST
# ============================================================================
print("7. DATABASE CONNECTION")
print("-" * 80)
try:
    from django.db import connections
    from django.db.utils import OperationalError

    db_conn = connections['default']

    # Try to connect
    try:
        cursor = db_conn.cursor()
        print(f"   ✓ Database connection successful")

        # Test query
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"   ✓ MySQL Version: {version[0]}")

        # Check if tables exist
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"   ✓ Tables in database: {len(tables)}")
        if len(tables) == 0:
            print(f"   ⚠ WARNING: No tables found - migrations may need to be run")
        else:
            print(f"   ✓ Sample tables: {', '.join([t[0] for t in tables[:5]])}")

        cursor.close()

    except OperationalError as e:
        print(f"   ✗ Database connection failed: {e}")
        print(f"\n   Possible issues:")
        print(f"      - Database credentials incorrect")
        print(f"      - Database server not running")
        print(f"      - Database user lacks permissions")
        print(f"      - Database does not exist")

except Exception as e:
    print(f"   ✗ Database test error: {e}")
    import traceback
    print(f"\n   Traceback:")
    print("   " + "\n   ".join(traceback.format_exc().split("\n")))
print()

# ============================================================================
# 8. CHECK STATIC FILES CONFIGURATION
# ============================================================================
print("8. STATIC FILES")
print("-" * 80)
try:
    from django.conf import settings

    print(f"   ✓ STATIC_URL: {settings.STATIC_URL}")
    print(f"   ✓ STATIC_ROOT: {settings.STATIC_ROOT}")

    static_root = Path(settings.STATIC_ROOT)
    if static_root.exists():
        print(f"   ✓ STATIC_ROOT exists")
        static_files = list(static_root.rglob('*'))
        print(f"   ✓ Static files collected: {len(static_files)} files")
    else:
        print(f"   ⚠ STATIC_ROOT does not exist - run collectstatic")

    print(f"   ✓ MEDIA_URL: {settings.MEDIA_URL}")
    print(f"   ✓ MEDIA_ROOT: {settings.MEDIA_ROOT}")

    media_root = Path(settings.MEDIA_ROOT)
    if media_root.exists():
        print(f"   ✓ MEDIA_ROOT exists")
    else:
        print(f"   ⚠ MEDIA_ROOT does not exist")

except Exception as e:
    print(f"   ✗ Static files check error: {e}")
print()

# ============================================================================
# 9. CHECK WSGI APPLICATION
# ============================================================================
print("9. WSGI APPLICATION")
print("-" * 80)
wsgi_file = BASE_DIR / 'passenger_wsgi.py'
if wsgi_file.exists():
    print(f"   ✓ passenger_wsgi.py exists")

    try:
        # Try to import the WSGI application
        sys.path.insert(0, str(BASE_DIR))
        from passenger_wsgi import application
        print(f"   ✓ WSGI application imported successfully")
        print(f"   ✓ Application type: {type(application)}")
    except Exception as e:
        print(f"   ✗ WSGI import error: {e}")
        import traceback
        print(f"\n   Traceback:")
        print("   " + "\n   ".join(traceback.format_exc().split("\n")))
else:
    print(f"   ✗ passenger_wsgi.py NOT FOUND")
print()

# ============================================================================
# 10. CHECK DIRECTORY PERMISSIONS
# ============================================================================
print("10. DIRECTORY PERMISSIONS")
print("-" * 80)
directories = {
    'Base Directory': BASE_DIR,
    'Static Root': getattr(settings, 'STATIC_ROOT', None),
    'Media Root': getattr(settings, 'MEDIA_ROOT', None),
    'Logs': BASE_DIR / 'logs',
}

for name, path in directories.items():
    if path and Path(path).exists():
        perms = oct(os.stat(path).st_mode)[-3:]
        readable = os.access(path, os.R_OK)
        writable = os.access(path, os.W_OK)
        executable = os.access(path, os.X_OK)

        status = "✓" if readable and writable and executable else "⚠"
        print(f"   {status} {name}: {perms} (R:{readable} W:{writable} X:{executable})")
    else:
        print(f"   ✗ {name}: NOT FOUND or not set")
print()

# ============================================================================
# SUMMARY
# ============================================================================
print("=" * 80)
print("DIAGNOSTIC SUMMARY")
print("=" * 80)
print()
print("If all checks passed (✓), your deployment should work.")
print("If you see errors (✗) or warnings (⚠), those need to be fixed.")
print()
print("Common fixes:")
print("  - Missing .env file: Copy .env.server to .env")
print("  - Database errors: Check credentials in .env file")
print("  - Missing tables: Run 'python manage.py migrate'")
print("  - Missing static files: Run 'python manage.py collectstatic'")
print("  - Permission errors: Run 'chmod 755' on directories and 'chmod 644' on files")
print()
print("After fixing issues, restart the application:")
print("  touch /home/wrgccpiz/public_html/nageshcare/passenger_wsgi.py")
print()
print("=" * 80)
