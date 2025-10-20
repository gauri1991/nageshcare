# Environment Configuration Comparison

**Date:** October 21, 2025
**Comparison:** Sumithrakp (Working) vs NageshCare (503 Error)

---

## CRITICAL DIFFERENCES FOUND

### 1. SSL/HTTPS Settings

| Setting | Sumithrakp (Working) | NageshCare (.env.server) | Impact |
|---------|---------------------|--------------------------|--------|
| `SECURE_SSL_REDIRECT` | **False** | **True** | Could cause redirect loop! |
| `SESSION_COOKIE_SECURE` | **False** | **True** | Session issues if SSL incomplete |
| `CSRF_COOKIE_SECURE` | **False** | **True** | CSRF validation failures |

**CRITICAL:** If SSL/HTTPS isn't 100% properly configured, forcing these to `True` can cause:
- 503 errors
- Redirect loops
- Session/cookie failures
- CSRF token mismatches

**Recommendation:** Start with SSL disabled (like sumithrakp), enable AFTER site works.

---

### 2. Database Configuration Method

| Method | Sumithrakp | NageshCare |
|--------|-----------|------------|
| Format | `DATABASE_URL` (single variable) | 6 separate `DB_*` variables |
| Library | Uses `dj-database-url` | Manual configuration |
| Example | `mysql://user:pass@host/db` | `DB_ENGINE=...`, `DB_NAME=...` |

**Impact:** More complex = more potential for errors

---

### 3. Extra Variables in NageshCare

| Variable | Sumithrakp | NageshCare | Needed? |
|----------|-----------|------------|---------|
| `DJANGO_ENV` | Not set | `production` | Optional |
| `CSRF_TRUSTED_ORIGINS` | Not set | Set | Only if SSL enabled |
| `STATIC_ROOT` | Uses default | Explicit path | Optional |
| `MEDIA_ROOT` | Uses default | Explicit path | Optional |

**Impact:** More variables = more complexity, more chances for conflicts

---

## RECOMMENDED TESTING STRATEGY

### Option 1: Minimal .env (Try This First!)

Use `.env.simplified` - matches working sumithrakp pattern:

```bash
SECRET_KEY=_qs_xg&$bt742ag7z%$j3bloue)xzxnt^^8fn-nod7mu@oa^q-
DEBUG=False
ALLOWED_HOSTS=nageshcare.com,www.nageshcare.com

DATABASE_URL=mysql://wrgccpiz_nageshcare_user:fxLF_4MxCCgvFP6@localhost:3306/wrgccpiz_nageshcare_db

# SSL DISABLED initially
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0
```

**Why:**
- ✅ Matches working site exactly
- ✅ Minimal variables
- ✅ SSL disabled initially (safer)
- ✅ Simpler database config

**But wait:** NageshCare settings don't support `DATABASE_URL` format yet!

---

### Option 2: Simplified .env with Separate DB Variables (RECOMMENDED)

Keep your current settings_prod.py, but simplify the .env:

```bash
# Django Settings
SECRET_KEY=_qs_xg&$bt742ag7z%$j3bloue)xzxnt^^8fn-nod7mu@oa^q-
DEBUG=False
ALLOWED_HOSTS=nageshcare.com,www.nageshcare.com

# Database (keep separate variables since settings_prod.py expects them)
DB_ENGINE=django.db.backends.mysql
DB_NAME=wrgccpiz_nageshcare_db
DB_USER=wrgccpiz_nageshcare_user
DB_PASSWORD=fxLF_4MxCCgvFP6
DB_HOST=localhost
DB_PORT=3306

# SSL - START DISABLED (like sumithrakp)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# Remove these (not needed initially):
# CSRF_TRUSTED_ORIGINS
# DJANGO_ENV (defaults to production anyway)
# STATIC_ROOT (uses default)
# MEDIA_ROOT (uses default)
```

**Why:**
- ✅ Works with existing settings_prod.py
- ✅ SSL disabled (safer)
- ✅ Removes unnecessary variables
- ✅ Closer to sumithrakp approach

---

## TESTING PLAN

### Phase 1: Get Site Working (No SSL)

1. **Use simplified .env** (SSL disabled)
2. **Deploy simplified passenger_wsgi.py**
3. **Place .htaccess in correct location** (`/public_html/`)
4. **Test site:** Should return HTTP 200, not 503

### Phase 2: Enable SSL (After Site Works)

Once site loads successfully:

```bash
# Update .env:
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://nageshcare.com,https://www.nageshcare.com
```

Restart application and test.

---

## LIKELY ROOT CAUSE

**The 503 error is probably caused by:**

1. **Primary:** .htaccess in wrong location (subdirectory vs parent) - **FIXED** ✅
2. **Secondary:** Over-complicated passenger_wsgi.py - **FIXED** ✅
3. **Tertiary:** SSL redirects enabled before SSL is fully working - **NEEDS TESTING** ⚠️

**Next Steps:**
1. Try deploying with `.env` that has SSL disabled (like sumithrakp)
2. If that works, then SSL settings were the problem
3. Then enable SSL gradually after confirming site works

---

## ENVIRONMENT FILE COMPARISON

### Sumithrakp .env (Working)
```bash
# 4 core variables
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=sumithrakp.com,www.sumithrakp.com,meenvstf.com
DATABASE_URL=mysql://user:pass@localhost/db

# SSL disabled
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_HSTS_SECONDS=0

# Total: 8 variables
```

### NageshCare .env.server (Not Working)
```bash
# Many variables
DJANGO_ENV=production
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=nageshcare.com,www.nageshcare.com
CSRF_TRUSTED_ORIGINS=https://nageshcare.com,https://www.nageshcare.com

# Database (6 variables)
DB_ENGINE=django.db.backends.mysql
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=localhost
DB_PORT=3306

# SSL enabled (could be the problem!)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Extra paths
STATIC_ROOT=/home/wrgccpiz/public_html/nageshcare/staticfiles
MEDIA_ROOT=/home/wrgccpiz/public_html/nageshcare/media
DEFAULT_FROM_EMAIL=...
SERVER_EMAIL=...
ADMIN_URL=admin/

# Total: 20+ variables
```

**Complexity Score:**
- Sumithrakp: 8 variables (simple)
- NageshCare: 20+ variables (complex)

**Complexity Ratio:** 2.5x more complex!

---

## RECOMMENDATION

Create `.env.testing` with minimal config:

```bash
SECRET_KEY=_qs_xg&$bt742ag7z%$j3bloue)xzxnt^^8fn-nod7mu@oa^q-
DEBUG=False
ALLOWED_HOSTS=nageshcare.com,www.nageshcare.com

DB_NAME=wrgccpiz_nageshcare_db
DB_USER=wrgccpiz_nageshcare_user
DB_PASSWORD=fxLF_4MxCCgvFP6

# SSL DISABLED (like sumithrakp)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

**Deploy this first.** If it works:
- SSL settings were the problem
- Gradually add back other settings one by one
- Enable SSL last

---

## SUMMARY

**Most Likely Root Causes (in order):**

1. ✅ **FIXED:** .htaccess in wrong directory
2. ✅ **FIXED:** Over-engineered passenger_wsgi.py
3. ⚠️ **TO TEST:** SSL redirects enabled too early
4. ⚠️ **TO TEST:** Too many environment variables causing conflicts

**Next Action:**
Test deployment with simplified .env (SSL disabled) to isolate the issue.
