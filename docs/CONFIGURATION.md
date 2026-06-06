# Configuration Guide - FoodDrop

This document provides detailed configuration instructions for the FoodDrop application.

## ⚙️ Environment Variables

### Basic Configuration

Create a `.env` file in the project root directory with the following variables:

```env
# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# Secret Key (generate with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
SECRET_KEY=your-secret-key-here

# Debug Mode (False in production)
DEBUG=True

# Allowed Hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (Gmail example)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email@gmail.com

# reCAPTCHA Keys (Optional but recommended)
RECAPTCHA_PUBLIC_KEY=your_public_key
RECAPTCHA_PRIVATE_KEY=your_private_key
```

### Production Configuration

```env
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com

# Database (Production PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=production_db
DB_USER=prod_user
DB_PASSWORD=strong_password_here
DB_HOST=your-db-host.example.com
DB_PORT=5432

# Email (SendGrid or similar)
EMAIL_BACKEND=sendgrid_backend.SendgridBackend
SENDGRID_API_KEY=your_sendgrid_key

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY=prod_public_key
RECAPTCHA_PRIVATE_KEY=prod_private_key
```

---

## 🔧 Django Settings Configuration

### settings.py Key Configurations

#### Installed Applications

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_recaptcha',
    'learnapp',
    'foods',
    'crispy_forms',
    'crispy_bootstrap5',
]
```

#### Database Configuration

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {'sslmode': 'require'},
    }
}
```

#### Media Files (User Uploads)

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

#### Static Files

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

#### Auto-Logout Configuration

```python
AUTO_LOGOUT = {
    'IDLE_TIME': 200,  # 200 seconds
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
}
```

#### Password Hashing

```python
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
```

#### Crispy Forms

```python
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
```

---

## 📧 Email Configuration

### Gmail Configuration

1. Enable 2-Step Verification on your Gmail account
2. Generate an App Password:
   - Visit [Google App Passwords](https://support.google.com/accounts/answer/185833)
   - Select "Mail" and "Windows Computer" (or your device)
   - Copy the generated password

3. Add to `.env`:
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   EMAIL_USE_TLS=True
   DEFAULT_FROM_EMAIL=your_email@gmail.com
   ```

### SendGrid Configuration

1. Create a SendGrid account and get your API key
2. Add to `.env`:
   ```env
   EMAIL_BACKEND=sendgrid_backend.SendgridBackend
   SENDGRID_API_KEY=your_sendgrid_key
   ```

### AWS SES Configuration

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=email-smtp.region.amazonaws.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_smtp_username
EMAIL_HOST_PASSWORD=your_smtp_password
EMAIL_USE_TLS=True
```

---

## 🔐 Security Configuration

### HTTPS/SSL Setup

For production, enable SSL/TLS:

```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}
```

### CSRF Protection

```python
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    # ... other middleware
]

CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://*.yourdomain.com',
]
```

### reCAPTCHA Integration

1. Get keys from [Google reCAPTCHA](https://www.google.com/recaptcha/admin)
2. Add to `.env`:
   ```env
   RECAPTCHA_PUBLIC_KEY=your_public_key
   RECAPTCHA_PRIVATE_KEY=your_private_key
   ```

3. Use in forms:
   ```python
   from django_recaptcha.fields import ReCaptchaField
   
   class MyForm(forms.Form):
       captcha = ReCaptchaField()
   ```

---

## 📊 Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/fooddrop.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

---

## 🚀 Production Deployment Checklist

```bash
# Pre-deployment verification
[ ] DEBUG = False in settings.py
[ ] ALLOWED_HOSTS configured correctly
[ ] SECRET_KEY changed and secure (not in version control)
[ ] Database migrations applied
[ ] Static files collected (collectstatic)
[ ] Email backend configured
[ ] SSL/HTTPS enabled
[ ] All environment variables set
[ ] Backups configured
[ ] Logging configured
[ ] Security headers set
[ ] CORS configured (if needed)
[ ] Rate limiting configured
[ ] Database optimized and indexed
[ ] Error monitoring setup (Sentry, etc.)
```

---

## 📱 Middleware Configuration

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

## 📚 Additional Resources

- [Django Settings Documentation](https://docs.djangoproject.com/en/5.2/topics/settings/)
- [Django Security](https://docs.djangoproject.com/en/5.2/topics/security/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)

