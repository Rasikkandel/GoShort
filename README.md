# GoShort - Production-Grade URL Shortener

A modern, scalable, and secure URL shortening service built with Django.

## Features

✨ **Core Features**
- Lightning-fast URL shortening with 6-character codes
- Click tracking and analytics
- Beautiful, responsive web interface
- Admin dashboard with statistics
- RESTful API (upcoming)

🔒 **Security**
- HTTPS/TLS encryption
- CSRF protection
- XSS prevention
- Security headers (HSTS, CSP)
- SQL injection prevention
- Rate limiting
- OWASP compliance

⚡ **Performance**
- PostgreSQL database
- Redis caching
- Gzip compression
- Static file optimization
- Database connection pooling
- Gunicorn WSGI server

🚀 **Deployment**
- Docker containerization
- Docker Compose orchestration
- Nginx reverse proxy
- SSL/TLS with Let's Encrypt
- Health checks
- Zero-downtime deployment ready

📊 **Monitoring**
- Structured logging
- Error tracking
- Application metrics
- Performance monitoring

## Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis (optional, for caching)
- Docker & Docker Compose (for containerized deployment)

### Local Development

```bash
# Clone repository
git clone <your-repo>
cd goshort

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000`

### Production Deployment

#### Option 1: Docker (Recommended)

```bash
# Update docker-compose.yml and .env
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py createsuperuser
```

#### Option 2: Manual VPS Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions.

#### Option 3: PaaS (Heroku, Railway, etc.)

See [DEPLOYMENT.md](DEPLOYMENT.md) for platform-specific guides.

## Configuration

### Environment Variables

```bash
# Core
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=goshort
DB_USER=db_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Cache
REDIS_URL=redis://localhost:6379/0
```

See `.env.example` for all available options.

## Project Structure

```
goshort/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker services configuration
├── nginx.conf              # Nginx reverse proxy config
├── gunicorn_config.py      # Gunicorn server config
├── DEPLOYMENT.md           # Deployment guide
├── shorturl/               # Main Django project
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI application
├── shorten/                # URL shortening app
│   ├── models.py           # Data models
│   ├── views.py            # View handlers
│   ├── urls.py             # App routing
│   └── admin.py            # Admin interface
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── links.html          # Links list page
│   ├── 404.html            # 404 error page
│   └── 500.html            # 500 error page
└── static/                 # Static assets
    ├── css/
    │   └── style.css       # Main stylesheet
    └── js/
        └── main.js         # JavaScript utilities
```

## API Endpoints

### Pages
- `GET /` - Home page (create new short URL)
- `GET /links/` - View all shortened URLs
- `GET /<short_code>/` - Redirect to original URL
- `/admin/` - Admin dashboard

### Admin
- `POST /admin/` - Admin login

## Admin Dashboard

Access admin panel at `/admin/` with superuser credentials.

**Features:**
- View all shortened URLs
- Edit URL information
- Reset click counts
- View detailed statistics
- Filter and search URLs
- Bulk actions

## Security Considerations

1. **Always use HTTPS** in production
2. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt`
3. **Change SECRET_KEY** - Generate unique key for each deployment
4. **Strong database password** - Use 16+ character random password
5. **Regular backups** - Implement automated database backups
6. **Monitor logs** - Watch for suspicious activity
7. **Update admin path** - Rename `/admin/` to something unique
8. **Rate limiting** - Enable to prevent abuse
9. **CORS configuration** - Restrict allowed origins
10. **SSL/TLS** - Use minimum TLS 1.2

## Monitoring & Logging

### Application Logs
```bash
# Local deployment
sudo journalctl -u goshort -f

# Docker deployment
docker-compose logs -f web
```

### Database Monitoring
```bash
# Connect to PostgreSQL
psql -U goshort_user -d goshort

# Check active connections
SELECT count(*) FROM pg_stat_activity;

# View slow queries
SELECT query, mean_time FROM pg_stat_statements ORDER BY mean_time DESC;
```

## Performance Optimization

1. **Enable Caching**
   - Redis for session storage
   - HTTP caching headers
   - Database query caching

2. **Database Optimization**
   - Add indexes on frequently searched columns
   - Use connection pooling
   - Regular VACUUM and ANALYZE

3. **Static Files**
   - Use CDN for distribution
   - Enable Gzip compression
   - Set far-future cache headers

4. **Monitoring**
   - Track request latency
   - Monitor database performance
   - Alert on error spikes

## Troubleshooting

### 502 Bad Gateway
```bash
# Check Gunicorn status
systemctl status goshort
docker-compose ps web

# View error logs
sudo journalctl -u goshort -n 50
```

### Static Files Not Loading
```bash
# Recollect static files
python manage.py collectstatic --clear --noinput

# Verify Nginx config
sudo nginx -t
```

### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -U goshort_user -h localhost -d goshort -c "SELECT 1"

# Check PostgreSQL service
sudo systemctl status postgresql
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions:
1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
2. Review Django documentation: https://docs.djangoproject.com/
3. Check Gunicorn docs: https://docs.gunicorn.org/
4. See Nginx docs: https://nginx.org/en/docs/

## Changelog

### v1.0.0 (2026-06-24)
- ✅ Initial release
- ✅ URL shortening feature
- ✅ Click tracking
- ✅ Beautiful UI with Bootstrap 5
- ✅ Admin dashboard
- ✅ Production-grade configuration
- ✅ Docker support
- ✅ Comprehensive documentation

## Acknowledgments

- Django Framework
- Bootstrap 5
- Font Awesome Icons
- PostgreSQL
- Nginx
- Gunicorn
