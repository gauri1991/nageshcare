# NageshCare Production Deployment Guide

Complete guide for deploying the NageshCare Django application to cPanel shared hosting.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup on cPanel](#initial-setup-on-cpanel)
3. [Environment Configuration](#environment-configuration)
4. [Database Setup](#database-setup)
5. [Deployment Process](#deployment-process)
6. [Development to Production Workflow](#development-to-production-workflow)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Local Development
- Python 3.8 or higher
- Git
- Virtual environment activated

### cPanel Requirements
- SSH access to your cPanel account
- Python app support (most shared hosting includes this)
- MySQL or PostgreSQL database access
- Domain configured and pointing to your hosting

---

## Initial Setup on cPanel

### 1. Access Your Server

SSH into your cPanel server:
```bash
ssh username@yourdomain.com
```

### 2. Clone the Repository

```bash
cd ~
git clone https://github.com/gauri1991/nageshcare.git
cd nageshcare
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Environment Configuration

### 1. Create `.env` File

Copy the example environment file:
```bash
cp .env.example .env
```

### 2. Edit `.env` with Production Values

```bash
nano .env
```

Update the following values:

```env
# Environment
DJANGO_ENV=production

# Security - Generate a new secret key!
SECRET_KEY=your-production-secret-key-here

# Debug - MUST be False in production
DEBUG=False

# Allowed Hosts - Your actual domain(s)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database (from cPanel MySQL database)
DB_ENGINE=django.db.backends.mysql
DB_NAME=username_nageshcare
DB_USER=username_nageshdb
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=3306

# Email (from cPanel email settings)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.yourdomain.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password

# Static/Media Paths (adjust to your cPanel username)
STATIC_ROOT=/home/username/public_html/nageshcare/static
MEDIA_ROOT=/home/username/public_html/nageshcare/media
```

**Important Notes:**
- Replace `username` with your actual cPanel username
- Replace `yourdomain.com` with your actual domain
- Generate a new SECRET_KEY using: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

### 3. Secure the `.env` File

```bash
chmod 600 .env
```

---

## Database Setup

### 1. Create MySQL Database in cPanel

1. Log into cPanel
2. Go to **MySQL Databases**
3. Create a new database (e.g., `username_nageshcare`)
4. Create a new database user
5. Add the user to the database with ALL PRIVILEGES
6. Note down the credentials for your `.env` file

### 2. Run Migrations

```bash
export DJANGO_ENV=production
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Load Initial Data (if any)

```bash
# If you have fixtures or initial data
python manage.py loaddata initial_data.json
```

---

## Deployment Process

### 1. Collect Static Files

Create the static files directory structure:
```bash
mkdir -p ~/public_html/nageshcare/static
mkdir -p ~/public_html/nageshcare/media
```

Collect static files:
```bash
python manage.py collectstatic --noinput
```

### 2. Setup Python App in cPanel

1. Log into cPanel
2. Go to **Setup Python App**
3. Click **Create Application**
4. Configure:
   - **Python version**: 3.8 or higher
   - **Application root**: `/home/username/nageshcare`
   - **Application URL**: Your domain
   - **Application startup file**: `passenger_wsgi.py`
   - **Application Entry point**: `application`

5. Click **Create**

### 3. Configure `.htaccess`

Copy the `.htaccess` file to your public_html:
```bash
cp .htaccess ~/public_html/
```

Edit it to update the paths:
```bash
nano ~/public_html/.htaccess
```

Replace `username` with your actual cPanel username.

### 4. Set Environment Variables in cPanel Python App

In the Python App configuration:
1. Click on your app
2. In the **Environment variables** section, add:
   - `DJANGO_ENV` = `production`

Or source the .env file by ensuring `passenger_wsgi.py` loads it (already configured).

### 5. Restart the Application

In cPanel Python App interface, click **Restart**.

Or via command line:
```bash
touch ~/nageshcare/passenger_wsgi.py
```

### 6. Verify Deployment

Visit your domain and check:
- [ ] Homepage loads correctly
- [ ] Static files (CSS, JS, images) are loading
- [ ] Admin panel is accessible at `/admin/`
- [ ] Forms work correctly
- [ ] Media uploads work

---

## Development to Production Workflow

### On Your Local Machine

#### 1. Develop and Test Locally

```bash
# Make sure you're using development settings
export DJANGO_ENV=development  # Or leave unset (development is default)

# Run local server
python manage.py runserver
```

#### 2. Commit Your Changes

```bash
git add .
git commit -m "Description of changes"
```

#### 3. Run the Deployment Script

```bash
./scripts/deploy.sh
```

This script will:
- Check for uncommitted changes
- Run tests (if configured)
- Check Python syntax
- Create a version tag (optional)
- Push to GitHub

### On Production Server

#### 1. SSH into Server

```bash
ssh username@yourdomain.com
cd ~/nageshcare
```

#### 2. Run the Update Script

```bash
./scripts/update_production.sh
```

This script will:
- Create a database backup
- Pull latest changes from GitHub
- Install/update dependencies
- Run migrations
- Collect static files
- Clear Python caches

#### 3. Restart the App

```bash
touch passenger_wsgi.py
```

Or use cPanel interface to restart.

---

## Quick Reference Commands

### Local Development
```bash
# Start development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Collect static files (dev)
python manage.py collectstatic
```

### Production Server
```bash
# Pull latest code
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations
DJANGO_ENV=production python manage.py migrate

# Collect static files
DJANGO_ENV=production python manage.py collectstatic --noinput

# Restart app
touch passenger_wsgi.py
```

---

## Troubleshooting

### Issue: Static files not loading

**Solution:**
1. Verify STATIC_ROOT path in `.env`
2. Check `.htaccess` configuration
3. Ensure permissions are correct:
   ```bash
   chmod 755 ~/public_html/nageshcare
   chmod 755 ~/public_html/nageshcare/static
   ```
4. Re-run collectstatic:
   ```bash
   python manage.py collectstatic --clear --noinput
   ```

### Issue: 500 Internal Server Error

**Solution:**
1. Check error logs:
   ```bash
   tail -f ~/nageshcare/logs/django.log
   tail -f ~/nageshcare/logs/error.log
   ```
2. Verify `.env` file exists and has correct values
3. Check database connection settings
4. Ensure `DJANGO_ENV=production` is set
5. Verify Python version compatibility

### Issue: Database connection error

**Solution:**
1. Verify database credentials in `.env`
2. Check database exists in cPanel
3. Verify user has permissions
4. Test connection:
   ```bash
   mysql -u username_nageshdb -p username_nageshcare
   ```

### Issue: Permission denied errors

**Solution:**
```bash
# Fix file permissions
find ~/nageshcare -type f -exec chmod 644 {} \;
find ~/nageshcare -type d -exec chmod 755 {} \;

# Make scripts executable
chmod +x ~/nageshcare/scripts/*.sh

# Secure .env
chmod 600 ~/nageshcare/.env
```

### Issue: ModuleNotFoundError

**Solution:**
1. Activate virtual environment:
   ```bash
   source ~/nageshcare/venv/bin/activate
   ```
2. Reinstall requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Restart the app

### Issue: CSRF verification failed

**Solution:**
1. Verify `CSRF_TRUSTED_ORIGINS` in `.env` includes your domain with https://
2. Check `ALLOWED_HOSTS` includes your domain
3. Clear browser cookies and try again

### Issue: Media uploads not working

**Solution:**
1. Create media directory:
   ```bash
   mkdir -p ~/public_html/nageshcare/media
   chmod 755 ~/public_html/nageshcare/media
   ```
2. Verify MEDIA_ROOT in `.env`
3. Check `.htaccess` has media alias configured

---

## Security Checklist

Before going live, ensure:

- [ ] `DEBUG=False` in production `.env`
- [ ] Unique `SECRET_KEY` generated for production
- [ ] `ALLOWED_HOSTS` set to specific domains only
- [ ] Database credentials are secure and unique
- [ ] `.env` file has 600 permissions (not world-readable)
- [ ] SSL/HTTPS is enabled (check `SECURE_SSL_REDIRECT`)
- [ ] Admin URL is protected or customized
- [ ] Regular backups are configured
- [ ] Error logging is enabled and monitored

---

## Backup Strategy

### Automated Backups

The `update_production.sh` script creates automatic backups before updates in the `backups/` directory.

### Manual Database Backup

```bash
# SQLite (if using)
cp db.sqlite3 backups/db_$(date +%Y%m%d_%H%M%S).sqlite3

# MySQL
mysqldump -u username_nageshdb -p username_nageshcare > backups/db_$(date +%Y%m%d_%H%M%S).sql
```

### Media Files Backup

```bash
tar -czf backups/media_$(date +%Y%m%d_%H%M%S).tar.gz ~/public_html/nageshcare/media/
```

---

## Support & Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **cPanel Documentation**: Contact your hosting provider
- **Project Repository**: https://github.com/gauri1991/nageshcare

For issues specific to this deployment, check the logs in `~/nageshcare/logs/` directory.
