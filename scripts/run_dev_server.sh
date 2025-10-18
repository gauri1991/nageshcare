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
echo "Checking port 8000..."
echo "========================================="

# Check if port 8000 is already in use
PORT_IN_USE=$(lsof -ti:8000 2>/dev/null)

if [ ! -z "$PORT_IN_USE" ]; then
    echo "⚠️  Port 8000 is already in use by process ID(s): $PORT_IN_USE"
    echo "Killing the process(es)..."
    kill -9 $PORT_IN_USE 2>/dev/null
    sleep 1

    # Verify the process was killed
    STILL_RUNNING=$(lsof -ti:8000 2>/dev/null)
    if [ -z "$STILL_RUNNING" ]; then
        echo "✓ Successfully killed process(es) on port 8000"
    else
        echo "❌ Failed to kill process on port 8000. Please kill it manually:"
        echo "   sudo kill -9 $STILL_RUNNING"
        exit 1
    fi
else
    echo "✓ Port 8000 is available"
fi

echo ""
echo "========================================="
echo "✓ Starting development server..."
echo "========================================="
echo ""

# Get local IP address for LAN access
LOCAL_IP=$(hostname -I | awk '{print $1}')

echo "📱 Local Access (this machine):"
echo "   http://127.0.0.1:8000/"
echo ""
echo "🌐 LAN Access (other devices on network):"
if [ ! -z "$LOCAL_IP" ]; then
    echo "   http://$LOCAL_IP:8000/"
else
    echo "   Unable to detect LAN IP"
fi
echo ""
echo "🔗 Quick Links:"
echo "   Admin: http://127.0.0.1:8000/admin/"
echo "   CMS:   http://127.0.0.1:8000/cms/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
python manage.py runserver 0.0.0.0:8000
