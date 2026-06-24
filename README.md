# GoShort - Production-Grade URL Shortener

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-GoShort-blue)](https://github.com/Rasikkandel/GoShort)
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9C%93-brightgreen)](https://opensource.org/)

A modern, scalable, and secure URL shortening service built with Django. 

**📢 Contributions Welcome!** We're looking for developers, designers, and documentation writers to help improve GoShort. See [Contributing](#contributing) to get started.

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

We welcome contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or helping with design, your contributions are valued.

### How to Contribute

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/GoShort.git
   cd GoShort
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Set up development environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   python manage.py migrate
   ```

4. **Make your changes**
   - Follow PEP 8 style guide
   - Write clear commit messages
   - Add tests for new features
   - Update documentation as needed

5. **Test your changes**
   ```bash
   python manage.py test
   python manage.py runserver
   ```

6. **Commit and push**
   ```bash
   git commit -m 'feat: Add amazing feature'
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots if UI changes are made

### Contribution Areas

We're looking for help with:
- 🐛 **Bug fixes** - Found an issue? Help us fix it!
- ✨ **New features** - Have a great idea? Implement it!
- 📚 **Documentation** - Help improve our guides and tutorials
- 🎨 **UI/UX improvements** - Enhance the design and usability
- 🧪 **Testing** - Add unit tests and integration tests
- 📦 **DevOps** - Improve deployment and CI/CD processes
- 🌍 **Internationalization** - Add support for multiple languages

### Reporting Issues

Found a bug? Have a suggestion? Please create an issue!

1. **Go to [Issues](https://github.com/Rasikkandel/GoShort/issues)**
2. **Click "New Issue"**
3. **Provide:**
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected behavior
   - Your environment (Django version, Python version, OS)
   - Screenshots if applicable

### Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help each other learn and grow

Unacceptable behavior includes:
- Harassment or discrimination
- Disrespectful language
- Personal attacks
- Spam or commercial promotion

Violations will be taken seriously and may result in removal from the project.

### Development Guidelines

- **Code Style**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **Django Best Practices**: Follow [Django documentation](https://docs.djangoproject.com/)
- **Commit Messages**: Use conventional commits (feat:, fix:, docs:, etc.)
- **Testing**: Aim for >80% code coverage
- **Documentation**: Update docs for new features

### Questions?

Join our discussions:
- 💬 [GitHub Discussions](https://github.com/Rasikkandel/GoShort/discussions)
- 📧 Create an issue with your question

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

### What MIT License Means
- ✅ **Free to use** - Personal, commercial, or educational use
- ✅ **Free to modify** - Change the code as you like
- ✅ **Free to distribute** - Share with others
- ⚠️ **Attribution required** - Include original copyright notice
- ⚠️ **No warranty** - Use at your own risk

## Creator

**Made with ❤️ by [Rasik Kandel](https://github.com/Rasikkandel)**

If you find this project useful, please:
- ⭐ **Star the repository** on GitHub
- 🔗 **Share** with others
- 🤝 **Contribute** to improve it
- 💬 **Provide feedback**

## Getting Help

### Documentation
- 📖 [DEPLOYMENT.md](DEPLOYMENT.md) - Complete deployment guide
- ⚡ [QUICKSTART.md](QUICKSTART.md) - Quick setup guides
- ✅ [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) - Pre-deployment checklist
- 📊 [PRODUCTION_SUMMARY.md](PRODUCTION_SUMMARY.md) - Production setup overview

### External Resources
- 🐍 [Django Documentation](https://docs.djangoproject.com/)
- 📚 [Gunicorn Docs](https://docs.gunicorn.org/)
- 🌐 [Nginx Docs](https://nginx.org/en/docs/)
- 🐘 [PostgreSQL Docs](https://www.postgresql.org/docs/)
- 📦 [Docker Docs](https://docs.docker.com/)

### Community Support
- 🐛 [Report Issues](https://github.com/Rasikkandel/GoShort/issues)
- 💬 [GitHub Discussions](https://github.com/Rasikkandel/GoShort/discussions)
- ⭐ [Star on GitHub](https://github.com/Rasikkandel/GoShort)

## Related Projects

Check out these similar open source projects:
- [Shorty](https://github.com/search?q=url+shortener&type=repositories)
- [Your Link Shortener](https://github.com/topics/url-shortener)

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

## Roadmap

We're planning the following features for future releases:

### v1.1.0 (Planned)
- [ ] RESTful API with authentication
- [ ] Custom short codes
- [ ] QR code generation
- [ ] Expiring links
- [ ] Link password protection
- [ ] Advanced analytics dashboard

### v1.2.0 (Planned)
- [ ] OAuth2 user authentication
- [ ] User accounts and link management
- [ ] API key management
- [ ] Webhook support
- [ ] Integration with third-party services

### v2.0.0 (Planned)
- [ ] Multi-tenant architecture
- [ ] Advanced caching strategies
- [ ] Machine learning based link recommendations
- [ ] Real-time analytics with WebSockets
- [ ] Mobile app (iOS/Android)

**Want to help with these features?** [Create an issue](https://github.com/Rasikkandel/GoShort/issues) or [start a discussion](https://github.com/Rasikkandel/GoShort/discussions)!

## Acknowledgments

**GoShort** is built on top of amazing open source projects:

### Core Framework
- 🐍 **Django** - Web framework for Python
- 🌐 **PostgreSQL** - Powerful, open source relational database
- 💾 **Redis** - In-memory data structure store
- 🌍 **Nginx** - High-performance web server
- 🚀 **Gunicorn** - Python WSGI HTTP Server

### Frontend
- 🎨 **Bootstrap 5** - CSS framework
- 📌 **Font Awesome** - Icon library
- ✨ **jQuery** - JavaScript library

### Development Tools
- 📦 **Docker** - Containerization platform
- 🔧 **Python** - Programming language
- 💻 **Git** - Version control

### Special Thanks
- Django community for excellent documentation
- Bootstrap team for beautiful components
- All open source contributors making this possible
- **GitHub** for hosting and collaboration tools

### Contributors
See [GitHub Contributors](https://github.com/Rasikkandel/GoShort/graphs/contributors) for the full list.

### Created By
**Rasik Kandel** - [GitHub Profile](https://github.com/Rasikkandel)

If you find this project helpful, please:
- ⭐ **Star this repository**
- 🔗 **Share with others**
- 🤝 **Contribute to the project**
- 💬 **Provide feedback**
