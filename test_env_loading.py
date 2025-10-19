#!/usr/bin/env python3
"""
Test script to verify environment variable loading on cPanel.
Upload this to your server and run it to debug .env file loading.
"""

import os
import sys

# Get the directory where this script is located
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(SITE_ROOT, '.env')

print("=" * 70)
print("ENVIRONMENT VARIABLE LOADING TEST")
print("=" * 70)
print(f"Script location: {SITE_ROOT}")
print(f"Looking for .env at: {env_file}")
print(f".env file exists: {os.path.exists(env_file)}")
print()

if os.path.exists(env_file):
    print(f"Reading .env file...")
    print("-" * 70)
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content[:500])  # Print first 500 chars
            if len(content) > 500:
                print(f"... (file continues, total {len(content)} bytes)")
    except Exception as e:
        print(f"ERROR reading file: {e}")
    print("-" * 70)
    print()

# Try loading with python-dotenv
print("Testing python-dotenv loading...")
try:
    from dotenv import load_dotenv
    load_dotenv(env_file, override=True)
    print("✓ python-dotenv loaded successfully")
except ImportError:
    print("✗ python-dotenv not available (will use fallback parser)")
except Exception as e:
    print(f"✗ Error loading with python-dotenv: {e}")
print()

# Test manual parsing
print("Testing manual parser...")
if os.path.exists(env_file):
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            loaded_vars = {}
            for line_num, line in enumerate(f, 1):
                original_line = line
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Parse key=value pairs
                if '=' in line:
                    # Handle comments at end of line
                    if '#' in line:
                        eq_pos = line.index('=')
                        hash_pos = line.index('#')
                        if hash_pos > eq_pos:
                            line = line[:hash_pos].strip()

                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Remove quotes if present
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]

                    if key:
                        loaded_vars[key] = value
                        os.environ[key] = value

        print(f"✓ Manually parsed {len(loaded_vars)} variables")
        print()
        print("Variables loaded:")
        for key in sorted(loaded_vars.keys()):
            # Mask sensitive values
            value = loaded_vars[key]
            if any(s in key.upper() for s in ['PASSWORD', 'SECRET', 'KEY']):
                display_value = value[:10] + "..." if len(value) > 10 else "***"
            else:
                display_value = value
            print(f"  {key} = {display_value}")
    except Exception as e:
        print(f"✗ Error in manual parsing: {e}")
        import traceback
        traceback.print_exc()
else:
    print("✗ .env file not found")

print()
print("=" * 70)
print("CHECKING REQUIRED ENVIRONMENT VARIABLES")
print("=" * 70)

required_vars = [
    'DJANGO_ENV',
    'SECRET_KEY',
    'DEBUG',
    'ALLOWED_HOSTS',
    'DB_ENGINE',
    'DB_NAME',
    'DB_USER',
    'DB_PASSWORD',
    'DB_HOST',
]

all_present = True
for var in required_vars:
    value = os.environ.get(var)
    if value:
        # Mask sensitive values
        if any(s in var for s in ['PASSWORD', 'SECRET', 'KEY']):
            display_value = value[:10] + "..." if len(value) > 10 else "***"
        else:
            display_value = value
        print(f"✓ {var} = {display_value}")
    else:
        print(f"✗ {var} = NOT SET")
        all_present = False

print()
if all_present:
    print("✓ All required environment variables are set!")
else:
    print("✗ Some required environment variables are missing!")

print("=" * 70)
