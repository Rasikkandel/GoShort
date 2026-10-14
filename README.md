# GoShort

GoShort is a small URL shortener built with Django. It creates short links,
counts visits, and shows the links in a simple dashboard.

## Run locally

Requirements: Python 3.12 or newer.

```bash
git clone <repository-url>
cd GoShort
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser.

The project uses SQLite, so no separate database or service is needed.

## Use the app

- `/` creates a short link.
- `/links/` lists all links and their click counts.
- `/<short-code>/` redirects to the original URL.
- `/admin/` opens the Django admin after creating a superuser with:

  ```bash
  python manage.py createsuperuser
  ```

## Run tests

```bash
python manage.py test
```

## Project layout

```text
shorturl/   Django project settings and URL configuration
shorten/    URL model, views, admin, and tests
templates/  HTML templates
static/     CSS and JavaScript
```

## License

This project is available under the MIT License. See [LICENSE](LICENSE).
