#!/bin/bash
# Development Server Startup Script for NageshCare
# This script activates the virtual environment and starts the Django development server

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "========================================="
echo "NageshCare Development Server"
echo "========================================="
echo ""

# Change to project root
cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please create it first: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if Django is installed
python -c "import django" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: Django not installed in virtual environment!"
    echo "Please install requirements: pip install -r requirements.txt"
    exit 1
fi

# Run migrations if needed
echo ""
echo "Checking for pending migrations..."
python manage.py migrate --check 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Pending migrations detected. Running migrations..."
    python manage.py migrate
fi

# Collect static files in production
# Uncomment the following lines if you want to collect static files on startup
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "✓ Starting development server..."
echo "========================================="
echo ""
echo "Access your site at: http://127.0.0.1:8000/"
echo "Admin panel at: http://127.0.0.1:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
python manage.py runserver 0.0.0.0:8000
