#!/bin/bash
# =====================================================
# Django to cPanel Deployment Script
# For: nageshcare.com
# cPanel User: wrgccpiz
# =====================================================

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
CPANEL_USER="wrgccpiz"
PROJECT_PATH="/home/${CPANEL_USER}/public_html/nageshcare"
VENV_PATH="/home/${CPANEL_USER}/virtualenv/public_html/nageshcare/3.12"
PYTHON_BIN="${VENV_PATH}/bin/python"
PIP_BIN="${VENV_PATH}/bin/pip"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Django cPanel Deployment Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Function to check command success
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1${NC}"
    else
        echo -e "${RED}✗ $1 failed${NC}"
        exit 1
    fi
}

# Step 1: Navigate to project directory
echo -e "${YELLOW}Step 1: Navigating to project directory...${NC}"
cd $PROJECT_PATH
check_status "Navigate to project directory"

# Step 2: Check if .env file exists
echo -e "${YELLOW}Step 2: Checking environment configuration...${NC}"
if [ ! -f ".env" ]; then
    if [ -f ".env.production" ]; then
        echo "Copying .env.production to .env..."
        cp .env.production .env
        check_status "Create .env from .env.production"
    else
        echo -e "${RED}✗ No .env file found! Please create it.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Step 3: Activate virtual environment
echo -e "${YELLOW}Step 3: Activating virtual environment...${NC}"
source ${VENV_PATH}/bin/activate
check_status "Activate virtual environment"

# Step 4: Install/Update dependencies
echo -e "${YELLOW}Step 4: Installing Python dependencies...${NC}"
${PIP_BIN} install --upgrade pip
${PIP_BIN} install -r requirements.txt
check_status "Install dependencies"

# Step 5: Run Django checks
echo -e "${YELLOW}Step 5: Running Django system checks...${NC}"
${PYTHON_BIN} manage.py check
check_status "Django system check"

# Step 6: Collect static files
echo -e "${YELLOW}Step 6: Collecting static files...${NC}"
${PYTHON_BIN} manage.py collectstatic --noinput --clear
check_status "Collect static files"

# Step 7: Run database migrations
echo -e "${YELLOW}Step 7: Running database migrations...${NC}"
${PYTHON_BIN} manage.py migrate --noinput
check_status "Database migrations"

# Step 8: Create logs directory if it doesn't exist
echo -e "${YELLOW}Step 8: Creating logs directory...${NC}"
mkdir -p logs
chmod 755 logs
check_status "Create logs directory"

# Step 9: Set proper permissions
echo -e "${YELLOW}Step 9: Setting file permissions...${NC}"

# Set directory permissions
find . -type d -exec chmod 755 {} \; 2>/dev/null

# Set file permissions
find . -type f -exec chmod 644 {} \; 2>/dev/null

# Make manage.py executable
chmod +x manage.py

# Secure sensitive files
chmod 600 .env 2>/dev/null
chmod 600 .env.production 2>/dev/null

# Make scripts executable
chmod +x deploy_to_cpanel.sh 2>/dev/null
chmod +x verify_deployment.py 2>/dev/null

check_status "Set file permissions"

# Step 10: Restart the application
echo -e "${YELLOW}Step 10: Restarting application...${NC}"
touch passenger_wsgi.py
check_status "Restart application"

# Step 11: Verify deployment
echo -e "${YELLOW}Step 11: Verifying deployment...${NC}"
if [ -f "verify_deployment.py" ]; then
    ${PYTHON_BIN} verify_deployment.py
else
    echo -e "${YELLOW}Skipping verification (verify_deployment.py not found)${NC}"
fi

# Final summary
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo "1. Visit https://nageshcare.com to verify the site is working"
echo "2. Check logs if there are any issues:"
echo "   - tail -f logs/passenger_error.log"
echo "   - tail -f logs/startup.log"
echo "   - tail -f logs/error.log"
echo ""
echo -e "${YELLOW}Important reminders:${NC}"
echo "- Ensure DEBUG=False in production"
echo "- Update SECRET_KEY with a secure value"
echo "- Configure email settings in .env"
echo "- Enable SSL redirect once SSL certificate is active"
echo ""