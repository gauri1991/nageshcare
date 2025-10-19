# NageshCare Wholesale Trading Website

A comprehensive Django-based website for NageshCare wholesale trading business, featuring a full CMS system, product management, and inquiry handling.

## Features

- **Custom CMS System**: Manage all website content without coding
  - Hero sections, features, testimonials
  - Product categories and listings
  - About, Contact, and Service pages
  - Policy pages (Privacy, Refund, Terms)

- **Product Management**: Complete CRUD operations for product catalog

- **Inquiry System**:
  - Contact form submissions
  - Quote requests
  - Email notifications
  - Admin reply system

- **Theme Customization**: Full color scheme control via CMS

- **SEO Optimized**: Meta tags, sitemaps, and search-friendly URLs

- **Responsive Design**: Bootstrap 5 with mobile-first approach

## Project Structure

```
nageshcare/
├── cms/                    # Custom CMS application
├── core/                   # Core pages (home, about, contact)
├── products/              # Product management
├── inquiries/             # Contact & quote inquiries
├── nageshcare_website/    # Project settings
│   ├── settings.py        # Main settings (auto-switches based on DJANGO_ENV)
│   ├── settings_base.py   # Shared settings
│   ├── settings_dev.py    # Development settings
│   └── settings_prod.py   # Production settings
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
├── media/                 # User-uploaded files
├── scripts/               # Deployment scripts
├── .env.example           # Environment variables template
├── passenger_wsgi.py      # cPanel Python app entry point
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
└── DEPLOYMENT.md          # Deployment guide
```

## Quick Start - Local Development

### 1. Clone the Repository

```bash
git clone https://github.com/gauri1991/nageshcare.git
cd nageshcare
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your local settings (or use defaults for development)
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit http://localhost:8000 to view the site.
Visit http://localhost:8000/admin to access the admin panel.

## Production Deployment

For complete deployment instructions to cPanel shared hosting, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Quick Deployment Workflow

**From Local Machine:**
```bash
# Make your changes and commit
git add .
git commit -m "Your changes"

# Run deployment script (checks, tests, and pushes to GitHub)
./scripts/deploy.sh
```

**On Production Server:**
```bash
# SSH into server
ssh username@yourdomain.com
cd ~/nageshcare

# Run update script (pulls code, migrates, collects static)
./scripts/update_production.sh

# Restart app
touch passenger_wsgi.py
```

## Environment Configuration

The project uses environment-based configuration:

- **Development** (default): Uses `settings_dev.py`
  - SQLite database
  - Debug mode enabled
  - Console email backend
  - Development tools (debug toolbar, django-extensions)

- **Production**: Uses `settings_prod.py`
  - MySQL/PostgreSQL database
  - Debug mode disabled
  - SMTP email backend
  - Enhanced security settings

Switch environments using the `DJANGO_ENV` variable:
```bash
export DJANGO_ENV=production  # For production
export DJANGO_ENV=development # For development (or leave unset)
```

## Key Management Commands

```bash
# Database
python manage.py migrate              # Run migrations
python manage.py makemigrations       # Create new migrations
python manage.py createsuperuser      # Create admin user

# Static Files
python manage.py collectstatic        # Collect static files

# Content Management
python manage.py dumpdata > backup.json   # Backup database
python manage.py loaddata backup.json     # Restore database

# Development
python manage.py runserver            # Start dev server
python manage.py shell               # Django shell
```

## Technology Stack

- **Framework**: Django 4.2+
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite (dev) / MySQL (production)
- **Forms**: django-crispy-forms with Bootstrap 5
- **Image Processing**: Pillow
- **Admin**: Django Admin with import/export
- **Server**: Gunicorn (production)

## Development Tools

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

Included tools:
- Django Debug Toolbar
- Django Extensions
- pytest for testing
- Code quality tools (black, flake8, isort)

## Project Settings Files

- **settings.py**: Auto-switches between dev/prod based on `DJANGO_ENV`
- **settings_base.py**: Common settings shared across environments
- **settings_dev.py**: Development-specific settings
- **settings_prod.py**: Production-specific settings with security hardening

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly in development
4. Commit with clear messages
5. Use `./scripts/deploy.sh` to push approved changes

## Security Notes

- Never commit `.env` files (they're in `.gitignore`)
- Always use unique `SECRET_KEY` for production
- Keep `DEBUG=False` in production
- Use HTTPS in production (configured in settings)
- Regularly update dependencies: `pip install -r requirements.txt --upgrade`

## Support

For deployment issues, see [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section.

For project-specific questions, check the code comments or contact the development team.

## License

Proprietary - NageshCare Wholesale Trading

---

**Last Updated**: October 2025
**Django Version**: 4.2+
**Python Version**: 3.8+
