#!/bin/bash
# =====================================================
# Production Environment Setup Script
# For: nageshcare.com
# This script helps set up the production environment
# =====================================================

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Production Environment Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to generate a secure Django secret key
generate_secret_key() {
    python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
}

# Check if .env exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file already exists!${NC}"
    echo -n "Do you want to overwrite it? (y/n): "
    read -r response
    if [ "$response" != "y" ]; then
        echo "Keeping existing .env file."
        exit 0
    fi
fi

# Start creating .env file
echo -e "${GREEN}Creating production .env file...${NC}"

# Get domain information
echo -n "Enter your primary domain (e.g., nageshcare.com): "
read -r DOMAIN
DOMAIN=${DOMAIN:-nageshcare.com}

# Generate secret key
echo -e "${YELLOW}Generating secure SECRET_KEY...${NC}"
SECRET_KEY=$(generate_secret_key 2>/dev/null || echo "django-insecure-PLEASE-CHANGE-THIS-KEY-$(date +%s)")

# Database configuration
echo -e "${BLUE}Database Configuration:${NC}"
echo -n "Database name [wrgccpiz_nageshcare_db]: "
read -r DB_NAME
DB_NAME=${DB_NAME:-wrgccpiz_nageshcare_db}

echo -n "Database user [wrgccpiz_nageshcare_user]: "
read -r DB_USER
DB_USER=${DB_USER:-wrgccpiz_nageshcare_user}

echo -n "Database password: "
read -rs DB_PASSWORD
echo ""

# Email configuration
echo -e "${BLUE}Email Configuration (optional):${NC}"
echo -n "Email host [smtp.hostinger.com]: "
read -r EMAIL_HOST
EMAIL_HOST=${EMAIL_HOST:-smtp.hostinger.com}

echo -n "Email address [info@${DOMAIN}]: "
read -r EMAIL_USER
EMAIL_USER=${EMAIL_USER:-info@${DOMAIN}}

echo -n "Email password (leave blank to skip): "
read -rs EMAIL_PASSWORD
echo ""

# SSL Configuration
echo -n "Enable SSL redirect? (y/n) [n]: "
read -r SSL_ENABLED
if [ "$SSL_ENABLED" = "y" ]; then
    SECURE_SSL_REDIRECT="True"
else
    SECURE_SSL_REDIRECT="False"
fi

# Create .env file
cat > .env << EOL
# Production Environment Configuration for ${DOMAIN}
# Generated on $(date)
# =====================================================

# Django Environment
DJANGO_ENV=production

# SECURITY WARNING: Keep this secret in production!
SECRET_KEY=${SECRET_KEY}

# Debug - MUST be False in production
DEBUG=False

# Allowed Hosts
ALLOWED_HOSTS=${DOMAIN},www.${DOMAIN},s6519.dnspark.in

# MySQL Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=localhost
DB_PORT=3306

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=${EMAIL_HOST}
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=${EMAIL_USER}
EMAIL_HOST_PASSWORD=${EMAIL_PASSWORD}
DEFAULT_FROM_EMAIL=${EMAIL_USER}
SERVER_EMAIL=admin@${DOMAIN}

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE=10485760
DATA_UPLOAD_MAX_MEMORY_SIZE=26214400

# Security Settings
SECURE_SSL_REDIRECT=${SECURE_SSL_REDIRECT}
EOL

if [ "$SECURE_SSL_REDIRECT" = "True" ]; then
    cat >> .env << EOL
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
EOL
fi

cat >> .env << EOL

# Static and Media Files - cPanel paths
STATIC_ROOT=/home/wrgccpiz/public_html/nageshcare/staticfiles
MEDIA_ROOT=/home/wrgccpiz/public_html/nageshcare/media

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://${DOMAIN},https://www.${DOMAIN}

# Admin URL (change for security)
ADMIN_URL=admin/
EOL

# Set proper permissions
chmod 600 .env

echo ""
echo -e "${GREEN}✓ .env file created successfully!${NC}"
echo ""
echo -e "${YELLOW}Important Next Steps:${NC}"
echo "1. Review the .env file and update any incorrect values"
echo "2. Ensure the database exists in cPanel MySQL"
echo "3. Run: ./deploy_to_cpanel.sh to deploy"
echo "4. Test the site at https://${DOMAIN}"
echo ""
echo -e "${RED}Security Reminders:${NC}"
echo "- Never commit .env to version control"
echo "- Keep SECRET_KEY confidential"
echo "- Use strong database passwords"
echo "- Enable SSL once certificate is installed"
echo ""