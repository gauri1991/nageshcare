#!/bin/bash
# Production update script - Run this on your cPanel server
# Usage: ./scripts/update_production.sh

set -e  # Exit on any error

echo "========================================="
echo "  Updating Production Environment"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}ERROR: manage.py not found. Are you in the project root?${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}ERROR: Virtual environment not found.${NC}"
    echo "Please create one with: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Verify we're in production mode
if [ "$DJANGO_ENV" != "production" ]; then
    echo -e "${YELLOW}WARNING: DJANGO_ENV is not set to 'production'${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create backup of database
echo ""
echo -e "${YELLOW}Creating database backup...${NC}"
BACKUP_DIR="backups"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup SQLite (if using)
if [ -f "db.sqlite3" ]; then
    cp db.sqlite3 "$BACKUP_DIR/db_backup_$TIMESTAMP.sqlite3"
    echo -e "${GREEN}✓ SQLite database backed up${NC}"
fi

# Pull latest changes
echo ""
echo -e "${YELLOW}Pulling latest changes from GitHub...${NC}"
git fetch origin
git pull origin main
echo -e "${GREEN}✓ Code updated${NC}"

# Install/update dependencies
echo ""
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt --upgrade
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Run migrations
echo ""
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate --noinput
echo -e "${GREEN}✓ Migrations completed${NC}"

# Collect static files
echo ""
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput --clear
echo -e "${GREEN}✓ Static files collected${NC}"

# Clear any caches
echo ""
echo -e "${YELLOW}Clearing caches...${NC}"
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo -e "${GREEN}✓ Caches cleared${NC}"

# Completion message
echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  Production update completed!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Final step: Restart the Python app in cPanel"
echo ""
echo "1. Log into cPanel"
echo "2. Go to 'Setup Python App'"
echo "3. Find your app and click 'Restart'"
echo ""
echo "Or use the command line if available:"
echo "  touch ~/nageshcare/passenger_wsgi.py"
echo ""
echo -e "${YELLOW}Backup created at: $BACKUP_DIR/db_backup_$TIMESTAMP.sqlite3${NC}"
echo ""
