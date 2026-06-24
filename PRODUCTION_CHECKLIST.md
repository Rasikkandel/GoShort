# Production Checklist for GoShort

## Pre-Deployment

- [ ] Generate new SECRET_KEY for production
  ```bash
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```
- [ ] Create `.env` file with production values
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set strong database password
- [ ] Generate SSL/TLS certificate
- [ ] Backup existing database (if migrating)

## Security

- [ ] Enable HTTPS/SSL
- [ ] Configure CSRF protection
  - [ ] Set `CSRF_TRUSTED_ORIGINS`
  - [ ] Update `CSRF_COOKIE_SECURE`
- [ ] Configure CORS if using API
- [ ] Set security headers
  - [ ] `SECURE_SSL_REDIRECT = True`
  - [ ] `SECURE_HSTS_SECONDS = 31536000`
  - [ ] `SECURE_BROWSER_XSS_FILTER = True`
- [ ] Disable admin at `/admin/` or rename it
- [ ] Use strong admin credentials
- [ ] Enable rate limiting
- [ ] Configure firewall rules
- [ ] Set up intrusion detection

## Database

- [ ] Create production database
- [ ] Create dedicated database user with limited privileges
- [ ] Test database connection
- [ ] Enable PostgreSQL SSL if remote
- [ ] Configure backup strategy
- [ ] Test backup and restore
- [ ] Enable query logging for monitoring
- [ ] Create database indexes
- [ ] Run `vacuum analyze` on database

## Application

- [ ] Run `python manage.py check --deploy`
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Create superuser
- [ ] Test all views and admin interface
- [ ] Configure error pages (404, 500)
- [ ] Set up logging
- [ ] Configure email for notifications

## Server

- [ ] Install and configure Gunicorn
- [ ] Install and configure Nginx
- [ ] Create systemd service file
- [ ] Test application startup
- [ ] Configure process manager (systemd/supervisor)
- [ ] Enable service auto-start
- [ ] Configure log rotation
- [ ] Set up monitoring and alerts

## Static Files

- [ ] Collect static files: `collectstatic`
- [ ] Configure Nginx to serve static files
- [ ] Set cache headers for static files
- [ ] Verify static files are loading
- [ ] Test CSS and JavaScript loading
- [ ] Compress images and assets
- [ ] Consider CDN for global delivery

## Performance

- [ ] Configure caching (Redis)
- [ ] Enable Gzip compression
- [ ] Configure database connection pooling
- [ ] Set Gunicorn worker count
- [ ] Enable HTTP/2
- [ ] Configure browser caching
- [ ] Test page load times
- [ ] Monitor query performance

## Monitoring

- [ ] Set up application logging
- [ ] Configure error monitoring (e.g., Sentry)
- [ ] Set up performance monitoring
- [ ] Create uptime monitoring alerts
- [ ] Configure email alerts for errors
- [ ] Set up log aggregation
- [ ] Enable slow query logging
- [ ] Create monitoring dashboard

## Backup & Recovery

- [ ] Automated database backups
- [ ] Test backup restoration
- [ ] Document backup procedure
- [ ] Store backups securely
- [ ] Document disaster recovery plan
- [ ] Test recovery process

## DNS & Domain

- [ ] Point domain to server
- [ ] Verify DNS resolution
- [ ] Test domain accessibility
- [ ] Check certificate for domain match
- [ ] Set up email records (MX)
- [ ] Configure SPF/DKIM if sending emails

## Documentation

- [ ] Document deployment steps
- [ ] Document system architecture
- [ ] Document backup/restore procedure
- [ ] Document monitoring setup
- [ ] Create runbook for common tasks
- [ ] Document emergency procedures
- [ ] Create admin guide
- [ ] Document API (if applicable)

## Final Testing

- [ ] Test main functionality (URL shortening)
- [ ] Test all links and navigation
- [ ] Test admin panel
- [ ] Test error pages
- [ ] Test on mobile devices
- [ ] Test with different browsers
- [ ] Load testing
- [ ] Security testing
- [ ] Test SSL certificate validity
- [ ] Verify HTTPS redirect

## Post-Deployment

- [ ] Monitor error logs for issues
- [ ] Check server resources (CPU, memory, disk)
- [ ] Verify email notifications working
- [ ] Create superuser for daily operations
- [ ] Document any custom configurations
- [ ] Set up scheduled maintenance tasks
- [ ] Create alerting rules
- [ ] Brief team on monitoring tools
- [ ] Schedule regular security updates
- [ ] Plan capacity scaling

## Rollback Plan

- [ ] Document rollback procedure
- [ ] Keep previous version available
- [ ] Test rollback process
- [ ] Document data migration path
- [ ] Prepare database restore script

---

## Verification Command

After deployment, run:

```bash
# Application checks
python manage.py check --deploy

# Database connectivity
python manage.py dbshell

# Static files
python manage.py collectstatic --noinput

# Create admin user if not done
python manage.py createsuperuser

# Test the application
curl -I https://yourdomain.com/
curl -I https://yourdomain.com/admin/
curl -I https://yourdomain.com/static/css/style.css
```

## Quick Command Reference

```bash
# Restart application
sudo systemctl restart goshort

# View logs
sudo journalctl -u goshort -f

# Collect static files
python manage.py collectstatic --noinput

# Database migration
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Clear cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

---

✅ Use this checklist before every production deployment!
