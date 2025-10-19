
text/x-generic .htaccess ( ASCII text )
# .htaccess for Django app on cPanel
# This file redirects all requests to the nageshcare subdirectory

# Force HTTPS (SSL)
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Redirect all requests to nageshcare subdirectory where the Python app lives
# Skip if already in nageshcare, or accessing static/media files
RewriteCond %{REQUEST_URI} !^/nageshcare/
RewriteCond %{REQUEST_URI} !^/static/
RewriteCond %{REQUEST_URI} !^/media/
RewriteCond %{REQUEST_URI} !^/staticfiles/
RewriteRule ^(.*)$ /nageshcare/$1 [L,PT]

# Configure Passenger to run the Python app from nageshcare subdirectory
PassengerEnabled on
PassengerAppRoot /home/wrgccpiz/public_html/nageshcare
PassengerStartupFile passenger_wsgi.py
PassengerPython /home/wrgccpiz/virtualenv/public_html/nageshcare/3.12/bin/python

# Serve static files directly
<IfModule mod_alias.c>
  Alias /static /home/wrgccpiz/public_html/nageshcare/static
  Alias /media /home/wrgccpiz/public_html/nageshcare/media
  Alias /staticfiles /home/wrgccpiz/public_html/nageshcare/staticfiles
</IfModule>

# Allow access to static and media files
<Directory "/home/wrgccpiz/public_html/nageshcare/static">
  Options -Indexes
  AllowOverride None
  Require all granted
</Directory>

<Directory "/home/wrgccpiz/public_html/nageshcare/media">
  Options -Indexes
  AllowOverride None
  Require all granted
</Directory>

<Directory "/home/wrgccpiz/public_html/nageshcare/staticfiles">
  Options -Indexes
  AllowOverride None
  Require all granted
</Directory>

# Security headers
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set X-Frame-Options "DENY"
  Header set X-XSS-Protection "1; mode=block"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>

# Prevent access to sensitive files
<FilesMatch "^\.">
  Require all denied
</FilesMatch>

<FilesMatch "\.(py|pyc|pyo|db|sqlite|sqlite3|log|ini|env)$">
  Require all denied
</FilesMatch>

# Cache static resources
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/gif "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType application/font-woff2 "access plus 1 year"
</IfModule>