# Correct cPanel Directory Structure for Django Deployment

**Based on:** Working sumithrakp.com configuration
**Date:** October 21, 2025

---

## CORRECT STRUCTURE (Sumithrakp - WORKING)

```
/home/meenvstf/
├── public_html/                              ← DOCUMENT ROOT
│   ├── .htaccess                             ✅ PASSENGER CONFIG HERE (parent)
│   ├── .well-known/
│   ├── 403.shtml
│   ├── 404.shtml
│   ├── robots.txt
│   └── sumithrakp/                           ← Django app subdirectory
│       ├── passenger_wsgi.py                 ✅ WSGI entry point
│       ├── manage.py
│       ├── requirements.txt
│       ├── .env                              ✅ Environment variables
│       ├── sumithrakp_website/               ← Django project
│       │   ├── settings.py
│       │   ├── urls.py
│       │   └── wsgi.py
│       ├── core/                             ← Django apps
│       ├── static/
│       ├── staticfiles/                      ✅ Collected static files
│       ├── media/
│       ├── templates/
│       └── (NO .htaccess in this directory)  ❌ NO .htaccess here!
│
└── virtualenv/
    └── public_html/
        └── sumithrakp/
            └── 3.11/
                ├── bin/python
                └── lib/python3.11/site-packages/
```

### Key Files:

**1. `/home/meenvstf/public_html/.htaccess`** (Parent directory)
```apache
# DO NOT REMOVE. CLOUDLINUX PASSENGER CONFIGURATION BEGIN
PassengerAppRoot "/home/meenvstf/public_html/sumithrakp"
PassengerBaseURI "/"
PassengerPython "/home/meenvstf/virtualenv/public_html/sumithrakp/3.11/bin/python"
# DO NOT REMOVE. CLOUDLINUX PASSENGER CONFIGURATION END

# Serve static files directly
RewriteEngine On
RewriteCond %{REQUEST_URI} ^/static/
RewriteRule ^static/(.*)$ /sumithrakp/staticfiles/$1 [L]
RewriteCond %{REQUEST_URI} ^/media/
RewriteRule ^media/(.*)$ /sumithrakp/media/$1 [L]
```

**2. `/home/meenvstf/public_html/sumithrakp/passenger_wsgi.py`** (Simple)
- 25 lines total
- No manual virtualenv setup
- No manual .env parsing
- Lets cPanel handle infrastructure

---

## INCORRECT STRUCTURE (NageshCare - NOT WORKING)

```
/home/wrgccpiz/
├── public_html/                              ← DOCUMENT ROOT
│   ├── (NO .htaccess - MISSING!)             ❌ MISSING .htaccess!
│   └── nageshcare/                           ← Django app subdirectory
│       ├── .htaccess                         ❌ WRONG! .htaccess in subdirectory
│       ├── passenger_wsgi.py                 ⚠️ Over-engineered (116 lines)
│       ├── manage.py
│       ├── requirements.txt
│       ├── .env
│       ├── nageshcare_website/
│       │   ├── settings.py
│       │   ├── settings_base.py
│       │   ├── settings_prod.py
│       │   └── settings_dev.py
│       ├── core/
│       ├── products/
│       ├── cms/
│       ├── inquiries/
│       ├── static/
│       ├── staticfiles/
│       ├── media/
│       └── templates/
│
└── virtualenv/
    └── public_html/
        └── nageshcare/
            └── 3.12/
                ├── bin/python
                └── lib/python3.12/site-packages/
```

### Problems:
1. ❌ .htaccess in `/nageshcare/` subdirectory (WRONG LOCATION)
2. ❌ NO .htaccess in `/public_html/` parent directory (MISSING)
3. ⚠️ Over-engineered passenger_wsgi.py (116 lines vs 25 lines)

---

## CORRECTED STRUCTURE (NageshCare - FIXED)

```
/home/wrgccpiz/
├── public_html/                              ← DOCUMENT ROOT
│   ├── .htaccess                             ✅ CREATED (Passenger config)
│   └── nageshcare/                           ← Django app subdirectory
│       ├── .htaccess.backup                  ✅ Old file backed up
│       ├── .htaccess.public_html             ✅ Template for parent directory
│       ├── passenger_wsgi.py                 ✅ SIMPLIFIED (31 lines)
│       ├── manage.py
│       ├── requirements.txt
│       ├── .env
│       ├── nageshcare_website/
│       │   ├── settings.py
│       │   ├── settings_base.py
│       │   ├── settings_prod.py              ✅ PyMySQL init here
│       │   └── settings_dev.py
│       ├── core/
│       ├── products/
│       ├── cms/
│       ├── inquiries/
│       ├── static/
│       ├── staticfiles/
│       ├── media/
│       └── templates/
│
└── virtualenv/
    └── public_html/
        └── nageshcare/
            └── 3.12/
                ├── bin/python
                └── lib/python3.12/site-packages/
```

### Fixed:
1. ✅ Created `.htaccess` in `/public_html/` (parent directory)
2. ✅ Removed `.htaccess` from `/nageshcare/` subdirectory
3. ✅ Simplified `passenger_wsgi.py` to 31 lines
4. ✅ Matches exact working pattern from sumithrakp

---

## KEY PRINCIPLE: WHERE DOES .htaccess GO?

### Rule:
**.htaccess MUST be in the PARENT directory (`public_html`), NOT in the app subdirectory**

### Why?
- Apache/Passenger needs to intercept requests at the document root level
- The .htaccess tells Apache "all requests for this domain → route to this Django app"
- If .htaccess is in the subdirectory, Apache never sees it for root domain requests

### Visual:

**WRONG:**
```
Request: https://nageshcare.com
  ↓
Apache looks at: /home/wrgccpiz/public_html/
  ↓
No .htaccess found! → Returns directory listing or 503
  ↓
Never reaches: /home/wrgccpiz/public_html/nageshcare/.htaccess
```

**CORRECT:**
```
Request: https://nageshcare.com
  ↓
Apache looks at: /home/wrgccpiz/public_html/
  ↓
Finds .htaccess with Passenger config
  ↓
Passenger routes to: /home/wrgccpiz/public_html/nageshcare/passenger_wsgi.py
  ↓
Django handles the request ✅
```

---

## COMPARISON TABLE

| Aspect | Sumithrakp (Working) | NageshCare Before | NageshCare After |
|--------|---------------------|-------------------|------------------|
| .htaccess location | `/public_html/` ✅ | `/nageshcare/` ❌ | `/public_html/` ✅ |
| .htaccess in app dir | None ✅ | 141 lines ❌ | None ✅ |
| passenger_wsgi.py | 25 lines ✅ | 116 lines ❌ | 31 lines ✅ |
| Manual virtualenv | No ✅ | Yes ❌ | No ✅ |
| Manual .env parsing | No ✅ | Yes ❌ | No ✅ |
| PyMySQL init | None (uses SQLite) | Twice ❌ | Once in settings ✅ |
| Complexity | Minimal ✅ | High ❌ | Minimal ✅ |

---

## DEPLOYMENT STEPS

### 1. Copy .htaccess to Correct Location
```bash
# On server:
cd /home/wrgccpiz/public_html/nageshcare
cp .htaccess.public_html /home/wrgccpiz/public_html/.htaccess
```

### 2. Verify Files are in Correct Locations
```bash
# Should exist:
ls -la /home/wrgccpiz/public_html/.htaccess                  # ✅ Parent directory
ls -la /home/wrgccpiz/public_html/nageshcare/passenger_wsgi.py  # ✅ App directory

# Should NOT exist:
ls -la /home/wrgccpiz/public_html/nageshcare/.htaccess       # ❌ Should be removed
```

### 3. Restart Application
```bash
touch /home/wrgccpiz/public_html/nageshcare/passenger_wsgi.py
```

### 4. Test
```bash
curl -I https://nageshcare.com
# Expected: HTTP/2 200 OK
```

---

## STATIC FILES ROUTING

### How it Works:

**Request:** `https://nageshcare.com/static/css/style.css`

**Flow:**
1. Apache receives request at `/public_html/`
2. Reads `/public_html/.htaccess`
3. Sees rewrite rule:
   ```apache
   RewriteCond %{REQUEST_URI} ^/static/
   RewriteRule ^static/(.*)$ /nageshcare/staticfiles/$1 [L]
   ```
4. Rewrites to: `/nageshcare/staticfiles/css/style.css`
5. Apache serves file directly (bypasses Django)

**Request:** `https://nageshcare.com/` (homepage)

**Flow:**
1. Apache receives request at `/public_html/`
2. Reads `/public_html/.htaccess`
3. Sees Passenger config:
   ```apache
   PassengerAppRoot "/home/wrgccpiz/public_html/nageshcare"
   PassengerBaseURI "/"
   ```
4. Routes to: `/nageshcare/passenger_wsgi.py`
5. Django handles the request

---

## COMMON MISTAKES TO AVOID

### ❌ Mistake 1: .htaccess in App Directory
```
/public_html/nageshcare/.htaccess  ← WRONG!
```
**Problem:** Apache doesn't see it when request comes to root domain

### ❌ Mistake 2: No .htaccess in Parent Directory
```
/public_html/ (no .htaccess)  ← WRONG!
```
**Problem:** Apache doesn't know how to route to Django app

### ❌ Mistake 3: Over-Complicated passenger_wsgi.py
```python
# Manual virtualenv setup
# Manual .env parsing
# Complex error logging
# 116 lines of code
```
**Problem:** Conflicts with cPanel's automatic setup

### ❌ Mistake 4: Duplicate Initialization
```python
# passenger_wsgi.py
pymysql.install_as_MySQLdb()

# settings_prod.py
pymysql.install_as_MySQLdb()  # ← Duplicate!
```
**Problem:** Can cause "already installed" errors

---

## SUMMARY

### The Golden Rules:
1. **One .htaccess only** - in `/public_html/` (parent), NOT in app subdirectory
2. **Simple passenger_wsgi.py** - Let cPanel handle virtualenv and environment
3. **Follow working pattern** - Copy what works (sumithrakp.com)
4. **Less is more** - Minimal code = fewer failure points

### Quick Checklist:
- [ ] .htaccess exists in `/home/wrgccpiz/public_html/`
- [ ] NO .htaccess in `/home/wrgccpiz/public_html/nageshcare/`
- [ ] passenger_wsgi.py is simple (under 50 lines)
- [ ] PassengerAppRoot points to `/home/wrgccpiz/public_html/nageshcare`
- [ ] PassengerBaseURI is set to `/`
- [ ] Static file rewrites point to `/nageshcare/staticfiles/$1`
- [ ] PyMySQL initialized only once (in settings_prod.py)

If all checkboxes are ✅, your deployment should work!
