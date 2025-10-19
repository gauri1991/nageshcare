#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Load environment variables from .env file before Django starts
    # This ensures environment variables are available for settings.py
    try:
        from dotenv import load_dotenv
        from pathlib import Path

        # Get the base directory (where manage.py is located)
        BASE_DIR = Path(__file__).resolve().parent
        env_file = BASE_DIR / '.env'

        if env_file.exists():
            load_dotenv(env_file, override=True)
    except ImportError:
        # Fallback to manual parsing if python-dotenv not available
        from pathlib import Path

        BASE_DIR = Path(__file__).resolve().parent
        env_file = BASE_DIR / '.env'

        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
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
                            # Only set if not already in environment
                            if key and key not in os.environ:
                                os.environ[key] = value
            except Exception:
                # Silently continue if .env can't be parsed
                pass

    # Configure PyMySQL to act as MySQLdb replacement for Django
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nageshcare_website.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
