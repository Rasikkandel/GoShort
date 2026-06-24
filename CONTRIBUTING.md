# Contributing to GoShort

Thank you for your interest in contributing to GoShort! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help each other learn and grow
- Report unacceptable behavior to the maintainers

Unacceptable behavior includes:
- Harassment or discrimination
- Disrespectful language
- Personal attacks
- Spam or commercial promotion

Violations will be taken seriously and may result in removal from the project.

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Git
- PostgreSQL (for database)
- Basic understanding of Django

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/GoShort.git
   cd GoShort
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/Rasikkandel/GoShort.git
   ```

## Development Setup

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # (if exists)
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your local database credentials
```

### 4. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
# Visit http://localhost:8000
```

## Making Changes

### Create a Feature Branch

Always create a new branch for your work:
```bash
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b fix/bug-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `perf/` - Performance improvements
- `test/` - Test additions/updates

### Commit Guidelines

Use clear, descriptive commit messages following conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `perf:` - Performance improvement
- `test:` - Test addition/update
- `chore:` - Maintenance

Examples:
```
feat(models): Add custom_domain field to ShortenedURL
fix(views): Prevent duplicate URL entries
docs(README): Add API documentation
```

## Submitting Changes

### Before Pushing

1. Update your branch with upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Run tests:
   ```bash
   python manage.py test
   ```

3. Check code style:
   ```bash
   flake8 shorten/
   black --check shorten/
   ```

### Push to Your Fork

```bash
git push origin your-branch-name
```

### Create a Pull Request

1. Go to GitHub and click "Compare & Pull Request"
2. Provide a clear title and description:
   - What problem does this solve?
   - How have you tested this?
   - Does this introduce breaking changes?
3. Link any related issues: "Closes #123"
4. Wait for review and address feedback

## Coding Standards

### Python Style

We follow PEP 8 with these tools:
- **Black** for formatting
- **Flake8** for linting
- **isort** for import sorting

### Django Best Practices

- Use Django ORM instead of raw SQL when possible
- Write efficient queries (avoid N+1 problems)
- Use Django's built-in security features
- Follow Django's app structure conventions
- Use meaningful variable and function names

### Code Style Guide

```python
# Good: Clear, readable code
def calculate_click_rate(url_id):
    url = ShortenedURL.objects.get(id=url_id)
    if url.total_clicks == 0:
        return 0.0
    return (url.unique_clicks / url.total_clicks) * 100

# Avoid: Unclear, hard to maintain
def calc(i):
    u = ShortenedURL.objects.get(id=i)
    return (u.u_c / u.t_c) * 100 if u.t_c else 0
```

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test shorten.tests.test_models

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests

Create tests in `shorten/tests/`:

```python
from django.test import TestCase
from shorten.models import ShortenedURL

class ShortenedURLTestCase(TestCase):
    def setUp(self):
        self.url = ShortenedURL.objects.create(
            long_url='https://example.com/very/long/url'
        )

    def test_short_code_generation(self):
        self.assertEqual(len(self.url.short_code), 6)
        self.assertTrue(self.url.short_code.isalnum())

    def test_click_tracking(self):
        initial_clicks = self.url.clicks
        self.url.clicks += 1
        self.url.save()
        self.assertEqual(self.url.clicks, initial_clicks + 1)
```

**Target:** Aim for >80% code coverage

## Documentation

### Update Documentation For:
- New features
- API changes
- Configuration options
- Deployment procedures

### Documentation Files
- `README.md` - Project overview
- `QUICKSTART.md` - Quick setup guides
- `DEPLOYMENT.md` - Deployment instructions
- `PRODUCTION_CHECKLIST.md` - Pre-deployment checklist
- Code comments - Complex logic explanation

### Writing Documentation

- Use clear, concise language
- Include examples and code snippets
- Keep it up-to-date with code changes
- Target non-experts as audience

## Types of Contributions

### 🐛 Bug Reports

Before submitting a bug report:
1. Check if issue already exists
2. Gather information:
   - Python version
   - Django version
   - OS and browser (for UI bugs)
   - Steps to reproduce
   - Expected behavior
   - Actual behavior

### ✨ Feature Requests

Provide:
- Clear use case/benefit
- Example of how it would work
- Potential implementation approach
- Any related issues

### 📚 Documentation

- Fix typos and unclear explanations
- Add missing documentation
- Create tutorials or guides
- Improve code examples

### 🎨 UI/UX Improvements

- Submit screenshots/mockups
- Explain the improvement
- Ensure responsive design
- Maintain accessibility standards

## Review Process

1. Maintainers will review your PR
2. Feedback will be provided for improvements
3. Make requested changes by pushing to your branch
4. Once approved, your PR will be merged

## Merging

Once your PR is approved:
- It will be merged to the main branch
- Your name will be added to contributors
- The change will be included in the next release

## Questions?

- 💬 [GitHub Discussions](https://github.com/Rasikkandel/GoShort/discussions)
- 🐛 [GitHub Issues](https://github.com/Rasikkandel/GoShort/issues)
- 📧 Create an issue with your question

## Recognition

All contributors are recognized in:
- Git commit history
- GitHub contributors page
- Release notes
- Project documentation

Thank you for contributing to GoShort! 🎉
