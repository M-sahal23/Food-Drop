# Troubleshooting Guide - FoodDrop

Common issues and their solutions for the FoodDrop application.

## 🚀 Installation & Setup Issues

### 1. Python Version Mismatch
**Error**: `Python 3.8+ required`

**Solution**:
```bash
# Check your Python version
python --version

# If you have multiple Python installations, use:
python3.8 --version
python3.9 --version
python3.10 --version

# Create virtual environment with specific Python version
python3.10 -m venv env1
```

---

### 2. Virtual Environment Activation Issues

**Error**: `'activate' is not recognized` or command not found

**Windows**:
```bash
# Use this command instead
env1\Scripts\activate

# Or use:
env1\Scripts\Activate.ps1
```

**macOS/Linux**:
```bash
source env1/bin/activate
```

**PowerShell**:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
env1\Scripts\Activate.ps1
```

---

### 3. Pip Install Fails
**Error**: `pip: command not found` or permission denied

**Solution**:
```bash
# Use Python module instead
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# For macOS/Linux with sudo
sudo pip install -r requirements.txt

# Try with --user flag
pip install --user -r requirements.txt
```

---

### 4. Missing Dependencies
**Error**: `ModuleNotFoundError: No module named 'django'`

**Solution**:
```bash
# Reinstall all dependencies
pip install --upgrade --force-reinstall -r requirements.txt

# Clear pip cache
pip cache purge

# Verify installation
python -c "import django; print(django.VERSION)"
```

---

## 🗄️ Database Issues

### 1. Database Connection Issues
**Error**: `could not connect to server: Connection refused`

**Solution**:
```bash
# Verify PostgreSQL is running
# Windows
services.msc  # Check PostgreSQL service

# macOS
brew services list

# Linux
sudo service postgresql status

# Test connection
python manage.py shell
>>> from django.db import connection
>>> connection.ensure_connection()
```

---

### 2. Database Authentication Failed
**Error**: `FATAL: Ident authentication failed for user "postgres"`

**Solution**:
1. Check `.env` file for correct credentials
2. Verify database user exists:
   ```bash
   # In PostgreSQL console
   psql -U postgres
   \du  # List users
   ```

3. Reset password:
   ```bash
   # In PostgreSQL console
   ALTER USER your_user WITH PASSWORD 'new_password';
   ```

---

### 3. Migration Errors
**Error**: `No such table: foods_fooditems`

**Solution**:
```bash
# Check migration status
python manage.py showmigrations

# Dry run to see what would be applied
python manage.py migrate --dry-run

# Apply all pending migrations
python manage.py migrate

# For specific app
python manage.py migrate foods

# Create new migrations after model changes
python manage.py makemigrations
python manage.py migrate
```

---

### 4. Migration Conflicts
**Error**: `Your models have changes that are not yet reflected in a migration`

**Solution**:
```bash
# Create new migration
python manage.py makemigrations

# Check for conflicts
python manage.py showmigrations

# If you need to rollback
python manage.py migrate foods zero  # Revert all migrations for foods app

# Reapply migrations
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Database Reset (Development Only)
**Warning**: This will delete all data!

```bash
# Delete database
rm db.sqlite3  # For SQLite

# Or for PostgreSQL
dropdb your_database_name
createdb your_database_name

# Recreate migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

## 🔐 Static & Media Files

### 1. Static Files Not Loading
**Error**: 404 errors for CSS/JS files

**Solution**:
```bash
# Collect static files
python manage.py collectstatic --clear --noinput --verbosity 2

# Check settings
# In settings.py, ensure:
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For development, ensure staticfiles are served
# urls.py should have:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

### 2. Media Upload Fails
**Error**: `Permission denied` when uploading files

**Solution**:
```bash
# Fix directory permissions
chmod -R 755 media/
chmod -R 755 static/

# For Linux/macOS, change ownership
chown -R www-data:www-data media/
chown -R www-data:www-data static/

# Ensure directories exist
mkdir -p media/foodimg
mkdir -p media/profile_pic
mkdir -p media/cartimg
mkdir -p media/sauces
mkdir -p media/toppings
mkdir -p media/baseimg
```

---

### 3. Image Upload Issues
**Error**: `The submitted data was not a valid image`

**Solution**:
```bash
# Install Pillow
pip install --upgrade Pillow

# Verify image formats are supported
python -c "from PIL import Image; print(Image.OPEN)"

# Check file permissions
chmod 644 media/foodimg/*
```

---

## 🛠️ Template & View Issues

### 1. Template Not Found
**Error**: `TemplateDoesNotExist: foods/allfoods.html`

**Solution**:
```bash
# Verify template path
python manage.py findstatic foods/allfoods.html

# Check TEMPLATES setting in settings.py:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        ...
    },
]

# Create missing template directories
mkdir -p templates/foods
mkdir -p templates/registration
```

---

### 2. Circular Import Error
**Error**: `ImportError: cannot import name 'X' from partially initialized module`

**Solution**:
```python
# Check for circular imports in models.py and views.py
# Avoid: from app import model_or_view at module level
# Instead: Import inside functions when needed

# Or use TYPE_CHECKING
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from other_app.models import MyModel
```

---

### 3. View Returns 500 Error
**Error**: `Internal Server Error`

**Solution**:
```bash
# Check error logs
python manage.py runserver  # Look at console output

# Enable debug logging
# settings.py:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Check debug.log file
tail -f debug.log
```

---

## 🔐 Authentication Issues

### 1. Login Fails
**Error**: `Invalid username or password`

**Solution**:
```bash
# Reset superuser password
python manage.py changepassword admin

# Create new superuser
python manage.py createsuperuser

# Check user in database
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()
>>> user = User.objects.get(username='admin')
>>> print(user.check_password('password'))
```

---

### 2. Session Expires Immediately
**Error**: User logged out after few seconds

**Solution**:
```python
# Increase session timeout in settings.py
SESSION_COOKIE_AGE = 86400 * 7  # 7 days in seconds

# Or disable auto-logout
AUTO_LOGOUT = {
    'IDLE_TIME': None,  # Disable idle logout
    'REDIRECT_TO_LOGIN_IMMEDIATELY': False,
}

# Clear existing sessions
python manage.py clearsessions
```

---

### 3. CSRF Token Error
**Error**: `Forbidden (403) CSRF token missing or incorrect`

**Solution**:
```html
<!-- Ensure CSRF token in forms -->
<form method="post">
  {% csrf_token %}
  <!-- form fields -->
</form>

# settings.py:
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
]

# Clear cookies
# Browser -> Settings -> Cookies -> Clear site data
```

---

## 💳 Payment Issues

### 1. Payment Gateway Connection Fails
**Error**: `ConnectionError: Payment gateway unreachable`

**Solution**:
```bash
# Check internet connection
ping google.com

# Verify payment gateway credentials
# .env file has correct API keys

# Test payment gateway connection
python manage.py shell
>>> import requests
>>> requests.get('https://api.paymentgateway.com/health')
```

---

### 2. Transaction Verification Fails
**Error**: `Transaction verification failed`

**Solution**:
```python
# Check transaction logs
# admin panel -> Transactions

# Verify API credentials
# .env:
PAYMENT_API_KEY=correct_key
PAYMENT_API_SECRET=correct_secret

# Test credentials
python manage.py shell
>>> from payments import verify_transaction
>>> verify_transaction('test_txn_id')
```

---

## 🧪 Testing Issues

### 1. Tests Fail
**Error**: `FAILED: tests.py::TestCase::test_method`

**Solution**:
```bash
# Run tests with verbose output
python manage.py test --verbosity=2

# Run specific test
python manage.py test foods.tests.FoodModelTest

# Run with keep database
python manage.py test --keepdb

# Run with debugging
python -m pdb manage.py test
```

---

### 2. Coverage Report Issues
**Error**: `coverage: error: No such file or directory`

**Solution**:
```bash
# Install coverage
pip install coverage

# Run coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# View HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

---

## 📊 Performance Issues

### 1. Slow Database Queries
**Error**: Application is slow, high CPU usage

**Solution**:
```bash
# Enable query logging
# settings.py (development only):
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        },
    },
}

# Analyze queries
python manage.py shell
>>> from django.db import connection
>>> from django.db import reset_queries
>>> settings.DEBUG = True

# Use django-debug-toolbar
pip install django-debug-toolbar
```

---

### 2. High Memory Usage
**Error**: Process uses too much RAM

**Solution**:
```bash
# Use database connection pooling
pip install psycopg2-pool

# Optimize queries - use select_related/prefetch_related
# models.py:
items = FoodItems.objects.select_related('category').all()

# Use pagination
from django.core.paginator import Paginator
paginator = Paginator(items, 20)
page_items = paginator.get_page(1)
```

---

## 🌐 Deployment Issues

### 1. Static Files Not Found in Production
**Error**: 404 for CSS/JS in production

**Solution**:
```bash
# Collect static files before deploying
python manage.py collectstatic --noinput

# Configure web server (Nginx/Apache)
# Nginx:
location /static/ {
    alias /path/to/staticfiles/;
}

location /media/ {
    alias /path/to/media/;
}
```

---

### 2. SSL Certificate Issues
**Error**: `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution**:
```python
# settings.py:
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Or properly configure SSL
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 📝 Debug Mode

### Enable Debug Logging
```python
# settings.py
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get logger in views
import logging
logger = logging.getLogger(__name__)
logger.debug("This is a debug message")
```

---

## 🆘 Getting Help

If you encounter issues not listed here:

1. Check [Django Documentation](https://docs.djangoproject.com/)
2. Search [Stack Overflow](https://stackoverflow.com/questions/tagged/django)
3. Open an issue on [GitHub](https://github.com/M-sahal23/Food-Drop/issues)
4. Check application logs in `debug.log`

---

## 📚 Additional Resources

- [Django Official Troubleshooting](https://docs.djangoproject.com/en/5.2/faq/)
- [PostgreSQL Troubleshooting](https://www.postgresql.org/docs/current/sql-syntax.html)
- [Bootstrap Issues](https://getbootstrap.com/docs/5.0/getting-started/introduction/)

