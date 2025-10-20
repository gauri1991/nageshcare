# cPanel Django Deployment Guide for NageshCare

## Configuration Files Fixed

### 1. `.htaccess` (Created in project root)
- Location: `/home/wrgccpiz/public_html/nageshcare/.htaccess`
- Purpose: Configure Passenger, routing, security, and caching
- Key features:
  - Passenger configuration for Python app
  - Static/media file serving rules
  - Security headers and file protection
  - Caching and compression

### 2. `passenger_wsgi.py` (Updated)
- Location: `/home/wrgccpiz/public_html/nageshcare/passenger_wsgi.py`
- Purpose: WSGI entry point for Passenger
- Key improvements:
  - Proper virtualenv path configuration
  - Automatic .env file loading
  - Error logging for debugging
  - MySQL driver compatibility

## Pre-Deployment Checklist

### On Your Local Machine:

1. **Prepare the production environment file**:
   ```bash
   # Copy .env.production to .env (locally for testing)
   cp .env.production .env
   ```

2. **Install production dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Collect static files**:
   ```bash
   python manage.py collectstatic --no-input
   ```

4. **Run migrations locally to test**:
   ```bash
   python manage.py migrate
   ```

5. **Test the configuration**:
   ```bash
   python manage.py check --deploy
   ```

## cPanel Deployment Steps

### Step 1: Upload Files to cPanel

1. **Via File Manager or FTP**:
   - Upload entire project to: `/home/wrgccpiz/public_html/nageshcare/`
   - Ensure `.htaccess` is in the root directory
   - Ensure `passenger_wsgi.py` is in the root directory

2. **Set File Permissions**:
   ```bash
   # Via cPanel Terminal or SSH
   cd /home/wrgccpiz/public_html/nageshcare

   # Set directory permissions
   find . -type d -exec chmod 755 {} \;

   # Set file permissions
   find . -type f -exec chmod 644 {} \;

   # Make manage.py executable
   chmod +x manage.py

   # Secure sensitive files
   chmod 600 .env
   chmod 600 .env.production

   # Create logs directory if not exists
   mkdir -p logs
   chmod 755 logs
   ```

### Step 2: Configure Environment

1. **Copy production environment file**:
   ```bash
   cp .env.production .env
   ```

2. **Edit .env file** with your actual values:
   ```bash
   nano .env
   ```
   Update:
   - `SECRET_KEY` - Generate a new one
   - `DB_PASSWORD` - Your actual database password
   - `EMAIL_HOST_PASSWORD` - Your email password
   - Verify all paths are correct

### Step 3: Set Up Python App in cPanel

1. **In cPanel > Setup Python App**:
   - Python version: 3.12 (or your version)
   - Application root: `public_html/nageshcare`
   - Application URL: Leave empty for root domain
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application`

2. **Install Python packages**:
   ```bash
   # Enter virtual environment
   source /home/wrgccpiz/virtualenv/public_html/nageshcare/3.12/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

### Step 4: Database Setup

1. **Create MySQL database in cPanel**:
   - Database name: `wrgccpiz_nageshcare_db`
   - Username: `wrgccpiz_nageshcare_user`
   - Grant all privileges

2. **Run migrations**:
   ```bash
   cd /home/wrgccpiz/public_html/nageshcare
   source /home/wrgccpiz/virtualenv/public_html/nageshcare/3.12/bin/activate
   python manage.py migrate
   ```

3. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

### Step 5: Static Files

1. **Collect static files**:
   ```bash
   python manage.py collectstatic --no-input
   ```

2. **Verify static files**:
   - Check if `/home/wrgccpiz/public_html/nageshcare/staticfiles/` exists
   - Contains admin/, css/, js/, images/ directories

### Step 6: Restart Application

1. **In cPanel Python App**:
   - Click "Restart" button

2. **Or via command line**:
   ```bash
   touch /home/wrgccpiz/public_html/nageshcare/passenger_wsgi.py
   ```

### Step 7: Verify Deployment

1. **Run verification script**:
   ```bash
   cd /home/wrgccpiz/public_html/nageshcare
   python verify_deployment.py
   ```

2. **Check error logs**:
   ```bash
   # Passenger error log
   tail -f logs/passenger_error.log

   # Django error log
   tail -f logs/error.log
   ```

## Troubleshooting Common Issues

### 1. 500 Internal Server Error

**Check**:
- `.env` file exists and has correct values
- Database credentials are correct
- Python packages installed in virtualenv
- File permissions are correct

**Debug**:
```bash
# Check passenger log
tail -n 50 logs/passenger_error.log

# Test Django directly
python manage.py runserver 0.0.0.0:8000
```

### 2. Static Files Not Loading

**Check**:
- `python manage.py collectstatic` was run
- `.htaccess` RewriteRules are correct
- `STATIC_ROOT` path in .env matches actual path

**Fix**:
```bash
python manage.py collectstatic --clear --no-input
```

### 3. Database Connection Error

**Check**:
- Database exists in cPanel
- User has privileges
- Password in .env is correct
- DB_HOST is 'localhost' (not 127.0.0.1)

**Test**:
```bash
python manage.py dbshell
```

### 4. Import Errors

**Check**:
- Virtual environment is activated
- All packages installed
- Python version matches

**Fix**:
```bash
pip install --upgrade -r requirements.txt
```

### 5. Admin CSS Not Loading

**Solution**:
```bash
python manage.py collectstatic --clear
# Ensure STATIC_ROOT is correctly set
```

## Important Security Notes

1. **After successful deployment**:
   - Change `DEBUG=False` in .env
   - Generate new `SECRET_KEY`
   - Enable HTTPS in .htaccess (uncomment SSL redirect)
   - Update `SECURE_SSL_REDIRECT=True` in .env

2. **Regular maintenance**:
   - Monitor logs regularly
   - Update packages periodically
   - Backup database regularly
   - Keep Django updated

## File Structure on cPanel

```
/home/wrgccpiz/
├── public_html/
│   └── nageshcare/           # Your Django project
│       ├── .htaccess          # Apache/Passenger config
│       ├── passenger_wsgi.py  # WSGI entry point
│       ├── .env               # Environment variables
│       ├── manage.py
│       ├── requirements.txt
│       ├── nageshcare_website/  # Django project directory
│       ├── cms/               # Django apps
│       ├── core/
│       ├── products/
│       ├── inquiries/
│       ├── static/            # Development static files
│       ├── staticfiles/       # Production static files (collected)
│       ├── media/             # User uploaded files
│       ├── templates/         # HTML templates
│       └── logs/              # Application logs
└── virtualenv/
    └── public_html/
        └── nageshcare/
            └── 3.12/          # Python virtual environment
```

## Quick Commands Reference

```bash
# Activate virtual environment
source /home/wrgccpiz/virtualenv/public_html/nageshcare/3.12/bin/activate

# Restart application
touch passenger_wsgi.py

# View logs
tail -f logs/error.log

# Django shell
python manage.py shell

# Check deployment
python manage.py check --deploy

# Collect static
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
```

## Support

If you encounter issues:
1. Check logs in `/home/wrgccpiz/public_html/nageshcare/logs/`
2. Run `verify_deployment.py` script
3. Ensure all paths in configuration files match your cPanel setup
4. Verify environment variables are loaded correctly