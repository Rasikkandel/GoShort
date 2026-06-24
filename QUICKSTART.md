# GoShort - Quick Start Guide

## 🚀 5-Minute Setup

### For Local Development

```bash
# 1. Clone the project
git clone <your-repo-url>
cd goshort

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
python manage.py migrate
python manage.py createsuperuser

# 5. Run development server
python manage.py runserver
```

Visit: `http://localhost:8000`

---

## 🐳 5-Minute Docker Deployment

```bash
# 1. Update environment
cp .env.example .env
nano .env  # Edit with your values

# 2. Build and deploy
docker-compose build
docker-compose up -d

# 3. Setup database
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# 4. Done! Visit https://yourdomain.com
```

---

## 🔐 Production Setup on VPS

```bash
# 1. SSH to your server
ssh user@your-server.com

# 2. Install dependencies
sudo apt-get update && sudo apt-get install -y \
  python3 python3-pip python3-venv postgresql nginx git

# 3. Clone project
cd /var/www
sudo git clone <your-repo-url> goshort
cd goshort

# 4. Setup Django app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env  # Configure

# 5. Initialize database
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

# 6. Setup Gunicorn service
sudo cp goshort.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable goshort
sudo systemctl start goshort

# 7. Setup Nginx
sudo cp nginx.conf /etc/nginx/sites-available/goshort
sudo nano /etc/nginx/sites-available/goshort  # Update domain
sudo ln -s /etc/nginx/sites-available/goshort /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 8. SSL Certificate (Let's Encrypt)
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com

# 9. Update Nginx config with SSL paths
sudo nano /etc/nginx/sites-available/goshort
sudo systemctl reload nginx

# 10. Done! Visit https://yourdomain.com
```

---

## 📋 Deployment Checklist

Before going live:

1. ✅ Update `.env` with production values
2. ✅ Generate new SECRET_KEY
3. ✅ Configure strong database password
4. ✅ Setup SSL/TLS certificate
5. ✅ Configure ALLOWED_HOSTS
6. ✅ Run `python manage.py check --deploy`
7. ✅ Create superuser account
8. ✅ Test all functionality
9. ✅ Verify logging is working
10. ✅ Setup automated backups

---

## 🔧 Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run Django shell
python manage.py shell

# Clear database (development only!)
python manage.py flush

# Restart application (systemd)
sudo systemctl restart goshort

# View logs
sudo journalctl -u goshort -f

# Docker commands
docker-compose up -d        # Start services
docker-compose down         # Stop services
docker-compose logs -f      # View logs
docker-compose ps          # Show status
```

---

## 📚 Documentation

- **Full Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Production Checklist**: [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)
- **Project README**: [README.md](README.md)

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Change port
python manage.py runserver 8001
```

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U goshort_user -d goshort
```

### Static Files Not Loading
```bash
# Recollect static files
python manage.py collectstatic --clear --noinput
```

### Permission Issues
```bash
# Fix permissions
sudo chown -R www-data:www-data /var/www/goshort
```

---

## 🎯 Next Steps

After successful deployment:

1. **Monitor**: Set up application monitoring
2. **Backup**: Schedule automated database backups
3. **Updates**: Plan regular security updates
4. **Scaling**: Monitor traffic and scale as needed
5. **Optimization**: Profile and optimize performance

---

## 💡 Tips

- **Development**: Use `DEBUG=True` only locally
- **Security**: Change `/admin/` path in production
- **Performance**: Enable Redis caching
- **Monitoring**: Use application monitoring tools
- **Backups**: Always have backup and recovery plan

---

## 🤝 Support

For issues or questions:
1. Check [DEPLOYMENT.md](DEPLOYMENT.md)
2. Review [README.md](README.md)
3. Consult [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)
4. Check Django documentation: https://docs.djangoproject.com/

---

Happy deploying! 🚀
