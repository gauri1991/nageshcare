# Migration Guide: Move App to /public_html Root

Since the main domain's document root cannot be changed in cPanel, we need to move the application files to `/home/wrgccpiz/public_html` (root directory).

## Steps to Migrate on Server:

### 1. Backup Current Setup
```bash
cd /home/wrgccpiz
cp -r public_html/nageshcare public_html/nageshcare_backup
```

### 2. Move Application Files to Root
```bash
cd /home/wrgccpiz/public_html/nageshcare

# Move all files to parent directory (public_html root)
mv * ../
mv .env ../ 2>/dev/null || true
mv .htaccess ../ 2>/dev/null || true
mv .gitignore ../ 2>/dev/null || true

# Go back to public_html
cd /home/wrgccpiz/public_html

# Remove empty nageshcare directory
rmdir nageshcare
```

### 3. Update Python App Configuration in cPanel
1. Go to **Setup Python App**
2. Click **Stop** on the current app
3. Click **Edit**
4. Change **App Root Directory** to: `/home/wrgccpiz/public_html`
5. Keep **App URI** as: `/`
6. Click **Update**
7. Click **Start**

### 4. Update Environment Variables
Edit `.env` file and update these paths:
```bash
STATIC_ROOT=/home/wrgccpiz/public_html/staticfiles
MEDIA_ROOT=/home/wrgccpiz/public_html/media
```

### 5. Recreate Directories
```bash
mkdir -p /home/wrgccpiz/public_html/logs
mkdir -p /home/wrgccpiz/public_html/media
mkdir -p /home/wrgccpiz/public_html/staticfiles
mkdir -p /home/wrgccpiz/public_html/tmp
```

### 6. Set Permissions
```bash
cd /home/wrgccpiz/public_html
chmod 755 .
chmod 755 manage.py passenger_wsgi.py
chmod 644 .htaccess
chmod -R 755 static media staticfiles logs
```

### 7. Collect Static Files Again
```bash
source /home/wrgccpiz/virtualenv/public_html/3.12/bin/activate
cd /home/wrgccpiz/public_html
python manage.py collectstatic --noinput
```

### 8. Restart Application
```bash
touch /home/wrgccpiz/public_html/passenger_wsgi.py
```

Or use cPanel → Setup Python App → Restart

### 9. Test
Visit: https://nageshcare.com

## Rollback (if needed):
```bash
cd /home/wrgccpiz/public_html
rm -rf * .*
cp -r nageshcare_backup/* .
cp -r nageshcare_backup/.* . 2>/dev/null || true
```

## After Migration Works:
```bash
# Remove backup
rm -rf /home/wrgccpiz/public_html/nageshcare_backup
```
