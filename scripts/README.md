# NageshCare Utility Scripts

This folder contains utility scripts for managing the NageshCare website.

## Available Scripts

### 1. populate_sample_data.py
**Purpose:** Populate the database with sample products and categories

**Usage:**
```bash
python scripts/populate_sample_data.py
```

**What it does:**
- Creates product categories (Personal Care, Wellness & Spiritual)
- Creates sample products (Premium Scented Tissue Papers, Authentic Dhoop Batti)
- Adds product variants and fragrance options
- Displays summary of created data

**Note:** Run this after completing migrations to get started with sample data.

---

### 2. backup_database.sh
**Purpose:** Create timestamped backups of the SQLite database

**Usage:**
```bash
bash scripts/backup_database.sh
# or
chmod +x scripts/backup_database.sh
./scripts/backup_database.sh
```

**What it does:**
- Creates a backup of db.sqlite3 with timestamp
- Stores backups in /backups directory
- Keeps only the last 10 backups automatically
- Shows backup size and location

**Backup location:** `/backups/db_backup_YYYYMMDD_HHMMSS.sqlite3`

---

### 3. run_dev_server.sh
**Purpose:** Start the Django development server with proper setup

**Usage:**
```bash
bash scripts/run_dev_server.sh
# or
chmod +x scripts/run_dev_server.sh
./scripts/run_dev_server.sh
```

**What it does:**
- Activates the virtual environment
- Checks for pending migrations and runs them
- Starts the development server on http://0.0.0.0:8000/
- Provides access URLs for the site and admin panel

**Access URLs:**
- Website: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

---

### 4. collect_static.sh
**Purpose:** Collect all static files to STATIC_ROOT directory

**Usage:**
```bash
bash scripts/collect_static.sh
# or
chmod +x scripts/collect_static.sh
./scripts/collect_static.sh
```

**What it does:**
- Activates virtual environment
- Runs Django's collectstatic command
- Copies all static files to STATIC_ROOT
- Required for production deployment

---

## Making Scripts Executable

To make shell scripts executable, run:

```bash
chmod +x scripts/*.sh
```

Then you can run them directly:

```bash
./scripts/run_dev_server.sh
./scripts/backup_database.sh
./scripts/collect_static.sh
```

---

## Quick Start Workflow

1. **Initial Setup:**
   ```bash
   # Create virtual environment
   python3 -m venv venv

   # Activate virtual environment
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Run migrations
   python manage.py migrate

   # Create superuser
   python manage.py createsuperuser

   # Populate sample data
   python scripts/populate_sample_data.py
   ```

2. **Daily Development:**
   ```bash
   # Start development server
   ./scripts/run_dev_server.sh

   # Or manually:
   source venv/bin/activate
   python manage.py runserver
   ```

3. **Before Deployment:**
   ```bash
   # Backup database
   ./scripts/backup_database.sh

   # Collect static files
   ./scripts/collect_static.sh
   ```

---

## Creating Custom Scripts

When creating new utility scripts:

1. **Python Scripts:**
   - Add Django setup code at the top
   - Use proper imports
   - Add helpful print statements
   - Follow the pattern in `populate_sample_data.py`

2. **Shell Scripts:**
   - Start with `#!/bin/bash`
   - Add comments explaining the script
   - Check for errors and provide feedback
   - Follow the pattern in existing `.sh` files

---

## Troubleshooting

**Virtual environment not found:**
```bash
python3 -m venv venv
```

**Permission denied on shell scripts:**
```bash
chmod +x scripts/*.sh
```

**Django not found:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Database locked error:**
- Stop the development server
- Close any admin panel sessions
- Try again

---

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Project Documentation: See /claude.md
- Admin Panel: http://127.0.0.1:8000/admin/ (when server is running)

---

**Note:** All scripts should be run from the project root directory or will automatically change to it.
