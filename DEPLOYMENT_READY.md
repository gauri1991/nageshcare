# NageshCare - Deployment Ready Configuration

## ✅ All Configurations Complete

### Project Details
- **Domain**: nageshcare.com
- **cPanel Username**: wrgccpiz
- **Application Path**: /home/wrgccpiz/public_html/nageshcare
- **Python Version**: 3.12
- **Database**: wrgccpiz_nageshcare_db
- **SSL**: Enabled

---

## Configuration Files Created/Updated

### 1. `.cpanel.yml` ✅
Automated deployment configuration for cPanel Git integration.

**What it does:**
- Copies files to deployment directory
- Installs Python dependencies
- Runs migrations
- Collects static files
- Restarts the application

### 2. `.env.example` ✅
Template for environment variables with correct database configuration.

**Key Settings:**
- Database: wrgccpiz_nageshcare_db
- User: wrgccpiz_nageshcare_user
- SSL: Enabled
- HTTPS: Enforced

### 3. `.htaccess` ✅
Apache/Passenger configuration with HTTPS enforcement.

**Features:**
- Passenger Python app configuration
- HTTPS redirect enabled
- Static/media file serving
- Security headers
- Performance optimization

### 4. `.gitignore` ✅
Comprehensive Django gitignore to protect sensitive files.

**Excludes:**
- .env files (except .env.example)
- Database files
- Logs and media
- Python cache files

### 5. `.env.server` ⚠️ (NOT in git)
Production environment file with **actual credentials**.

**Contains:**
- Real database password
- Generated SECRET_KEY
- Production-ready settings

---

## Deployment Instructions

### On cPanel (First Time Setup)

1. **Create Python App in cPanel**
   - Go to: Setup Python App
   - Python Version: 3.12
   - Application Root: `/home/wrgccpiz/public_html/nageshcare`
   - Application URL: Leave empty (root domain)
   - Application Entry Point: `passenger_wsgi.py`

2. **Set up Git Deployment** (Optional)
   - Go to: Git Version Control
   - Create/Clone repository
   - Pull from: git@github.com:gauri1991/nageshcare.git
   - Branch: main

3. **Upload/Sync Files**
   - Upload all files to `/home/wrgccpiz/public_html/nageshcare/`
   - Or use Git pull if configured

4. **Copy Environment File**
   ```bash
   cd /home/wrgccpiz/public_html/nageshcare
   cp .env.server .env
   chmod 600 .env
   ```

5. **Activate Virtual Environment**
   ```bash
   source /home/wrgccpiz/virtualenv/public_html/nageshcare/3.12/bin/activate
   ```

6. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

7. **Run Django Setup**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

8. **Create Required Directories**
   ```bash
   mkdir -p logs media staticfiles
   chmod 755 logs media staticfiles
   ```

9. **Restart Application**
   ```bash
   touch passenger_wsgi.py
   ```

### Test Your Deployment

Visit: https://nageshcare.com

Expected results:
- ✅ Site loads via HTTPS
- ✅ Static files (CSS/JS/Images) load
- ✅ Admin panel accessible: https://nageshcare.com/admin/
- ✅ No 500 errors in logs

---

## Important Files Reference

### Files in Git Repository
```
.cpanel.yml          - Automated deployment config
.env.example         - Environment template
.gitignore          - Git exclusions
.htaccess           - Apache configuration
passenger_wsgi.py   - WSGI entry point
requirements.txt    - Python dependencies
manage.py           - Django management
nageshcare_website/ - Django settings
cms/                - Apps
core/
products/
inquiries/
static/             - Static source files
templates/          - HTML templates
```

### Files NOT in Git (Protected)
```
.env                - Production secrets (use .env.server)
.env.server         - Template with real values
db.sqlite3          - Local database
logs/               - Application logs
media/              - User uploads
staticfiles/        - Collected static files
venv/               - Virtual environment
```

---

## Database Configuration

**Database Name:** wrgccpiz_nageshcare_db
**Username:** wrgccpiz_nageshcare_user
**Password:** (in .env.server file)
**Host:** localhost
**Port:** 3306

---

## Virtual Environment Path

```bash
/home/wrgccpiz/virtualenv/public_html/nageshcare/3.12
```

**Activation command:**
```bash
source /home/wrgccpiz/virtualenv/public_html/nageshcare/3.12/bin/activate && cd /home/wrgccpiz/public_html/nageshcare
```

---

## Troubleshooting

### Check Logs
```bash
tail -f /home/wrgccpiz/public_html/nageshcare/logs/django.log
tail -f /home/wrgccpiz/public_html/nageshcare/logs/passenger_error.log
```

### Restart Application
```bash
touch /home/wrgccpiz/public_html/nageshcare/passenger_wsgi.py
```

### Verify Settings
```bash
python manage.py check --deploy
```

### Recollect Static Files
```bash
python manage.py collectstatic --clear --noinput
```

---

## Next Steps After Deployment

1. ✅ Test all pages and functionality
2. ✅ Configure email settings (when ready)
3. ✅ Set up regular database backups
4. ✅ Monitor logs for errors
5. ✅ Consider custom admin URL for security

---

**Deployment Date:** Ready for deployment
**Django Version:** 4.2.25
**Python Version:** 3.12
