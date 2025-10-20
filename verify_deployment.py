#!/usr/bin/env python
"""
Deployment verification script for Django on cPanel
Run this to check if your configuration is correct.
"""

import os
import sys
import json
from pathlib import Path

def check_paths():
    """Check if critical paths exist"""
    print("\n=== Checking Paths ===")
    issues = []

    # Update these paths according to your cPanel setup
    paths_to_check = {
        'Project Home': '/home/wrgccpiz/public_html/nageshcare',
        'Virtual Env': '/home/wrgccpiz/virtualenv/public_html/nageshcare/3.12',
        'Python Binary': '/home/wrgccpiz/virtualenv/public_html/nageshcare/3.12/bin/python',
        'Static Root': '/home/wrgccpiz/public_html/nageshcare/staticfiles',
        'Media Root': '/home/wrgccpiz/public_html/nageshcare/media',
    }

    for name, path in paths_to_check.items():
        if os.path.exists(path):
            print(f"✓ {name}: {path}")
        else:
            print(f"✗ {name}: {path} - NOT FOUND")
            issues.append(f"{name} path not found")

    return issues

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n=== Checking Environment File ===")
    issues = []

    env_path = '/home/wrgccpiz/public_html/nageshcare/.env'

    if not os.path.exists(env_path):
        print(f"✗ .env file not found at: {env_path}")
        issues.append(".env file missing")
        return issues

    print(f"✓ .env file found at: {env_path}")

    # Check for required environment variables
    required_vars = [
        'SECRET_KEY',
        'DJANGO_ENV',
        'DEBUG',
        'ALLOWED_HOSTS',
        'DB_ENGINE',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'STATIC_ROOT',
        'MEDIA_ROOT',
    ]

    with open(env_path, 'r') as f:
        env_content = f.read()

    print("\nRequired environment variables:")
    for var in required_vars:
        if var in env_content:
            print(f"✓ {var}")
        else:
            print(f"✗ {var} - NOT FOUND")
            issues.append(f"Missing environment variable: {var}")

    return issues

def check_django_imports():
    """Check if Django can be imported"""
    print("\n=== Checking Django Installation ===")
    issues = []

    try:
        import django
        print(f"✓ Django installed: {django.get_version()}")
    except ImportError:
        print("✗ Django not installed or not in Python path")
        issues.append("Django import failed")
        return issues

    # Try to load settings
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')
        from django.conf import settings
        print("✓ Django settings can be loaded")

        # Check critical settings
        print(f"  - DEBUG: {settings.DEBUG}")
        print(f"  - ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"  - STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"  - MEDIA_ROOT: {settings.MEDIA_ROOT}")

    except Exception as e:
        print(f"✗ Failed to load Django settings: {e}")
        issues.append(f"Django settings error: {str(e)}")

    return issues

def check_database():
    """Check database connection"""
    print("\n=== Checking Database Connection ===")
    issues = []

    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')
        import django
        django.setup()

        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✓ Database connection successful")
            else:
                print("✗ Database query failed")
                issues.append("Database query failed")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        issues.append(f"Database error: {str(e)}")

    return issues

def check_static_files():
    """Check if static files are collected"""
    print("\n=== Checking Static Files ===")
    issues = []

    static_root = '/home/wrgccpiz/public_html/nageshcare/staticfiles'

    if not os.path.exists(static_root):
        print(f"✗ Static root directory not found: {static_root}")
        issues.append("Static root directory missing")
        return issues

    # Check for admin static files (usually a good indicator)
    admin_css = os.path.join(static_root, 'admin', 'css', 'base.css')
    if os.path.exists(admin_css):
        print("✓ Admin static files found")
    else:
        print("✗ Admin static files not found - run 'python manage.py collectstatic'")
        issues.append("Static files not collected")

    # Count static files
    static_count = sum([len(files) for r, d, files in os.walk(static_root)])
    print(f"  Total static files: {static_count}")

    return issues

def main():
    print("="*60)
    print("Django cPanel Deployment Verification")
    print("="*60)

    all_issues = []

    # Run all checks
    all_issues.extend(check_paths())
    all_issues.extend(check_env_file())
    all_issues.extend(check_django_imports())
    all_issues.extend(check_database())
    all_issues.extend(check_static_files())

    # Summary
    print("\n" + "="*60)
    if all_issues:
        print("DEPLOYMENT ISSUES FOUND:")
        print("-"*60)
        for i, issue in enumerate(all_issues, 1):
            print(f"{i}. {issue}")
        print("\nPlease fix these issues before deploying.")
    else:
        print("✓ All checks passed! Your deployment configuration looks good.")
    print("="*60)

if __name__ == "__main__":
    # Add project to path
    project_home = '/home/wrgccpiz/public_html/nageshcare'
    if project_home not in sys.path:
        sys.path.insert(0, project_home)

    main()