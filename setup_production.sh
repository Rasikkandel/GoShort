#!/bin/bash
# Production startup script for GoShort

set -e

echo "🚀 Starting GoShort Production Setup..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and update values"
    exit 1
fi

# Load environment
source .env

echo "📦 Installing dependencies..."
pip install --quiet -r requirements.txt

echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

echo "📂 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create superuser: python manage.py createsuperuser"
echo "2. Start Gunicorn: gunicorn --config gunicorn_config.py shorturl.wsgi:application"
echo "3. Or use Docker: docker-compose up -d"
echo ""
echo "Visit: https://yourdomain.com"
echo "Admin: https://yourdomain.com/admin"
