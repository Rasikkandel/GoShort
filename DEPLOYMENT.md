# Production Deployment Guide for GoShort

## Pre-Deployment Checklist

### 1. Environment Setup
```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env with your production values
nano .env
```

**Required environment variables:**
- `DEBUG=False`
- `SECRET_KEY=your-secure-key-here` (Generate with: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
- `DB_PASSWORD=strong-password`
- `CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com`

### 2. Database Setup

**Option A: Local PostgreSQL**
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres createdb goshort
sudo -u postgres createuser goshort_user
sudo -u postgres psql

psql# ALTER USER goshort_user WITH PASSWORD 'strong-password';
psql# ALTER ROLE goshort_user SET client_encoding TO 'utf8';
psql# ALTER ROLE goshort_user SET default_transaction_isolation TO 'read committed';
psql# ALTER ROLE goshort_user SET default_transaction_deferrable TO ON;
psql# ALTER ROLE goshort_user SET timezone TO 'UTC';
psql# GRANT ALL PRIVILEGES ON DATABASE goshort TO goshort_user;
psql# \q
```

**Option B: Docker (Recommended)**
```bash
docker-compose up -d db
```

### 3. Static Files Setup

```bash
# Collect static files
python manage.py collectstatic --noinput

# Or with Docker
docker-compose run web python manage.py collectstatic --noinput
```

### 4. Database Migrations

```bash
# Apply migrations
python manage.py migrate

# Or with Docker
docker-compose run web python manage.py migrate
```

### 5. Create Superuser

```bash
# Create admin user
python manage.py createsuperuser

# Or with Docker
docker-compose run web python manage.py createsuperuser
```

---

## Deployment Methods

### Method 1: Docker (Recommended)

#### Prerequisites
- Docker and Docker Compose installed
- Domain with SSL certificate (or use Let's Encrypt)

#### Steps

1. **Update Configuration**
```bash
# Update docker-compose.yml with your values
# - Database password
# - Django SECRET_KEY
# - ALLOWED_HOSTS
# - Domain names
```

2. **Generate SSL Certificates**
```bash
# Using Let's Encrypt with Certbot
docker run --rm -v $(pwd)/ssl:/etc/letsencrypt certbot/certbot certonly \
  --standalone -d yourdomain.com -d www.yourdomain.com
```

3. **Build and Run**
```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f web
```

4. **Verify Services**
```bash
# Check if all containers are running
docker-compose ps

# Test the application
curl https://yourdomain.com/
```

---

### Method 2: Manual Deployment on VPS (Ubuntu/Debian)

#### Prerequisites
- VPS with Ubuntu 20.04+
- Python 3.9+
- PostgreSQL
- Nginx
- SSL certificate

#### Installation Steps

1. **System Updates**
```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip python3-venv postgresql nginx git
```

2. **Clone Repository**
```bash
cd /var/www
sudo git clone <your-repo> goshort
cd goshort
sudo chown -R $(whoami):$(whoami) .
```

3. **Setup Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
nano .env  # Edit with your values
```

5. **Setup Database**
```bash
# Configure PostgreSQL (see Database Setup section above)
```

6. **Run Migrations**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

7. **Setup Gunicorn**
```bash
# Test Gunicorn
gunicorn --config gunicorn_config.py shorturl.wsgi:application

# Create systemd service
sudo nano /etc/systemd/system/goshort.service
```

Add the following content:
```ini
[Unit]
Description=GoShort Gunicorn Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/goshort
Environment="PATH=/var/www/goshort/venv/bin"
ExecStart=/var/www/goshort/venv/bin/gunicorn --config gunicorn_config.py shorturl.wsgi:application

[Install]
WantedBy=multi-user.target
```

8. **Enable and Start Gunicorn**
```bash
sudo systemctl daemon-reload
sudo systemctl enable goshort
sudo systemctl start goshort
sudo systemctl status goshort
```

9. **Configure Nginx**
```bash
# Copy nginx config
sudo cp nginx.conf /etc/nginx/sites-available/goshort

# Enable site
sudo ln -s /etc/nginx/sites-available/goshort /etc/nginx/sites-enabled/

# Update domain in config
sudo nano /etc/nginx/sites-available/goshort

# Test and reload Nginx
sudo nginx -t
sudo systemctl reload nginx
```

10. **SSL Certificate (Let's Encrypt)**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com
```

---

### Method 3: Platform as a Service (PaaS)

#### Heroku Deployment

1. **Install Heroku CLI**
```bash
curl https://cli.heroku.com/install.sh | sh
heroku login
```

2. **Create Heroku App**
```bash
heroku create goshort-app
```

3. **Add PostgreSQL Addon**
```bash
heroku addons:create heroku-postgresql:standard-0
```

4. **Set Environment Variables**
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=goshort-app.herokuapp.com
```

5. **Deploy**
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## Post-Deployment

### Health Checks

```bash
# Test main application
curl https://yourdomain.com/

# Test health endpoint
curl https://yourdomain.com/health

# Check admin panel
https://yourdomain.com/admin/
```

### Monitoring

1. **View Logs**
```bash
# Local deployment
sudo journalctl -u goshort -f

# Docker deployment
docker-compose logs -f web
```

2. **Monitor Performance**
```bash
# Check system resources
htop

# Database queries
python manage.py shell
>>> from django.db import connection
>>> print(connection.queries)
```

### Backup Strategy

```bash
# Database backup
pg_dump -U goshort_user goshort > backup_$(date +%Y%m%d).sql

# Restore
psql -U goshort_user goshort < backup_20240624.sql

# Automated backup (cron job)
0 2 * * * /path/to/backup.sh
```

---

## Security Best Practices

1. **Change Default Credentials**
   - Update database passwords
   - Change admin username
   - Update SECRET_KEY regularly

2. **Enable HTTPS**
   - Use SSL/TLS certificates
   - Enable HSTS headers
   - Redirect HTTP to HTTPS

3. **Firewall Rules**
   - Allow only necessary ports (80, 443)
   - Restrict admin panel access
   - Use fail2ban for DDoS protection

4. **Regular Updates**
   - Keep Django updated
   - Update all dependencies
   - Monitor security advisories

5. **Logging & Monitoring**
   - Enable application logging
   - Monitor error logs
   - Set up alerts for errors

---

## Troubleshooting

### 502 Bad Gateway
```bash
# Check if Gunicorn is running
systemctl status goshort
docker-compose ps web

# Check logs
sudo journalctl -u goshort -n 50
docker-compose logs web
```

### Static Files Not Loading
```bash
# Recollect static files
python manage.py collectstatic --clear --noinput

# Check permissions
ls -la /var/www/goshort/staticfiles/

# Verify Nginx config
sudo nginx -t
```

### Database Connection Issues
```bash
# Test connection
psql -U goshort_user -h localhost -d goshort

# Check PostgreSQL status
sudo systemctl status postgresql

# View PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql.log
```

---

## Performance Optimization

1. **Database Optimization**
   - Add database indexes
   - Use connection pooling
   - Enable query caching

2. **Caching**
   - Enable Redis caching
   - Cache static assets (30+ days)
   - Cache database queries

3. **Code Optimization**
   - Use select_related() for foreign keys
   - Use prefetch_related() for reverse relations
   - Implement pagination

4. **Server Configuration**
   - Increase Gunicorn workers
   - Enable Gzip compression
   - Use CDN for static files

---

## Support & Documentation

- Django: https://docs.djangoproject.com/
- Gunicorn: https://docs.gunicorn.org/
- Nginx: https://nginx.org/en/docs/
- PostgreSQL: https://www.postgresql.org/docs/
- Docker: https://docs.docker.com/
