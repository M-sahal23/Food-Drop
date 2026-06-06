# Deployment Guide - FoodDrop

Complete guide for deploying FoodDrop to production environments.

## 🚀 Deployment Checklist

Before deploying to production:

```
[ ] DEBUG = False in settings.py
[ ] ALLOWED_HOSTS configured properly
[ ] SECRET_KEY is strong and unique
[ ] Database migrations applied successfully
[ ] Static files collected (python manage.py collectstatic)
[ ] Email backend configured
[ ] SSL/HTTPS certificate installed
[ ] Environment variables properly set
[ ] Database backups configured
[ ] Error monitoring setup (Sentry, etc.)
[ ] Security headers configured
[ ] CORS configured (if needed)
[ ] Rate limiting configured
[ ] Database indexed and optimized
[ ] All dependencies in requirements.txt
[ ] .env.example updated with new variables
```

---

## 🌐 Recommended Hosting Platforms

| Platform | Best For | Price | Setup Time |
|----------|----------|-------|-----------|
| **Heroku** | Rapid deployment, auto-scaling | $7-50/mo | 5 min |
| **DigitalOcean** | Full control, VPS | $5-40/mo | 30 min |
| **AWS/EC2** | Large scale, enterprise | Variable | 1-2 hours |
| **Google Cloud** | High performance, ML | Variable | 1-2 hours |
| **Render** | Modern, easy deployment | $7+/mo | 10 min |
| **PythonAnywhere** | Python-specific | $5-50/mo | 15 min |
| **Railway** | Developer-friendly | Pay as you go | 10 min |
| **Fly.io** | Global deployment | Pay as you go | 15 min |

---

## 🚀 Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

### Setup

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Procfile**
   ```
   # Procfile
   web: gunicorn LEARNING.wsgi
   release: python manage.py migrate
   ```

4. **Create runtime.txt** (optional, specifies Python version)
   ```
   python-3.10.2
   ```

5. **Update requirements.txt**
   ```bash
   pip freeze > requirements.txt
   # Add gunicorn if not present
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

6. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

7. **Configure environment variables**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   heroku config:set DB_ENGINE=django.db.backends.postgresql
   heroku config:set DB_NAME=your_db_name
   # ... add more config vars
   ```

8. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

9. **Deploy**
   ```bash
   git push heroku main
   ```

10. **Create superuser**
    ```bash
    heroku run python manage.py createsuperuser
    ```

11. **Access app**
    ```
    https://your-app-name.herokuapp.com
    ```

---

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "LEARNING.wsgi"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: fooddrop_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - DB_ENGINE=django.db.backends.postgresql
      - DB_NAME=fooddrop_db
      - DB_USER=postgres
      - DB_PASSWORD=your_password
      - DB_HOST=db
      - DB_PORT=5432
    depends_on:
      - db

volumes:
  postgres_data:
```

### Deploy with Docker
```bash
# Build image
docker build -t fooddrop:latest .

# Run container
docker run -p 8000:8000 fooddrop:latest

# Or use docker-compose
docker-compose up -d
```

---

## 🖥️ DigitalOcean Deployment

### Prerequisites
- DigitalOcean account
- Droplet with Ubuntu 20.04+

### Setup

1. **Create Droplet**
   - Size: $5-10/month basic option
   - Image: Ubuntu 20.04
   - Add SSH key

2. **SSH into Droplet**
   ```bash
   ssh root@your_droplet_ip
   ```

3. **Update System**
   ```bash
   apt update && apt upgrade -y
   apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/M-sahal23/Food-Drop.git
   cd Food-Drop
   ```

5. **Setup Python Environment**
   ```bash
   python3 -m venv env1
   source env1/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

6. **Configure PostgreSQL**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE fooddrop_db;
   CREATE USER fooddrop_user WITH PASSWORD 'strong_password';
   ALTER ROLE fooddrop_user SET client_encoding TO 'utf8';
   GRANT ALL PRIVILEGES ON DATABASE fooddrop_db TO fooddrop_user;
   \q
   ```

7. **Create .env file**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your settings
   ```

8. **Run Migrations**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

9. **Create Systemd Service File**
   ```bash
   sudo nano /etc/systemd/system/fooddrop.service
   ```
   
   ```ini
   [Unit]
   Description=FoodDrop Django Application
   After=network.target

   [Service]
   Type=notify
   User=root
   WorkingDirectory=/root/Food-Drop
   ExecStart=/root/Food-Drop/env1/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 LEARNING.wsgi
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

10. **Enable and Start Service**
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable fooddrop
    sudo systemctl start fooddrop
    sudo systemctl status fooddrop
    ```

11. **Configure Nginx**
    ```bash
    sudo nano /etc/nginx/sites-available/fooddrop
    ```
    
    ```nginx
    server {
        listen 80;
        server_name your_domain.com www.your_domain.com;

        location = /favicon.ico { access_log off; log_not_found off; }
        
        location /static/ {
            alias /root/Food-Drop/staticfiles/;
        }

        location /media/ {
            alias /root/Food-Drop/media/;
        }

        location / {
            include proxy_params;
            proxy_pass http://127.0.0.1:8000;
        }
    }
    ```

12. **Enable Nginx Site**
    ```bash
    sudo ln -s /etc/nginx/sites-available/fooddrop /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

13. **Setup SSL with Let's Encrypt**
    ```bash
    sudo apt install certbot python3-certbot-nginx -y
    sudo certbot --nginx -d your_domain.com
    ```

14. **Access Application**
    ```
    https://your_domain.com
    Admin: https://your_domain.com/admin
    ```

---

## 🔐 Production Security Configuration

### settings.py for Production
```python
# Security Settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS/SSL
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Security Headers
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
    'style-src': ("'self'", "'unsafe-inline'", "cdn.jsdelivr.net"),
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/fooddrop/django.log',
            'maxBytes': 1024*1024*10,
            'backupCount': 5,
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'WARNING',
    }
}
```

---

## 📊 Database Backups

### PostgreSQL Automated Backups
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups/fooddrop"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="fooddrop_db"

mkdir -p $BACKUP_DIR

pg_dump -h localhost -U fooddrop_user $DB_NAME | gzip > "$BACKUP_DIR/backup_$TIMESTAMP.sql.gz"

# Keep only last 7 days of backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/backup_$TIMESTAMP.sql.gz"
```

### Schedule with Cron
```bash
# Add to crontab
crontab -e

# Run daily at 2 AM
0 2 * * * /path/to/backup.sh
```

---

## 🔄 Continuous Deployment

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

---

## 📈 Monitoring & Analytics

### Setup Error Monitoring (Sentry)
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False
)
```

### Setup Monitoring
- Use New Relic
- Use DataDog
- Use Scout APM

---

## 🚨 Troubleshooting Deployment

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database Connection Fails
```bash
# Check connection string in .env
# Verify database is running
# Check firewall rules
```

### Application Won't Start
```bash
# Check logs
heroku logs --tail  # For Heroku

# Check systemd logs
sudo journalctl -u fooddrop -n 50  # For DigitalOcean
```

---

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Heroku Documentation](https://devcenter.heroku.com/)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

