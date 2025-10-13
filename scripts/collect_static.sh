#!/bin/bash
# Collect Static Files Script for NageshCare
# This script collects all static files to the STATIC_ROOT directory

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================="
echo "NageshCare - Collect Static Files"
echo "========================================="
echo ""

# Change to project root
cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Collect static files
echo "Collecting static files to STATIC_ROOT..."
echo ""

python manage.py collectstatic --noinput

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Static files collected successfully!"
    echo ""
    echo "Static files location: $(python manage.py diffsettings | grep STATIC_ROOT | cut -d '=' -f2)"
else
    echo "❌ Error: Failed to collect static files!"
    exit 1
fi

exit 0
