#!/bin/bash
# Docker deployment script

set -e

echo "🐳 GoShort Docker Deployment Script"
echo "===================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose found"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env with your configuration"
    exit 1
fi

echo "🔨 Building Docker images..."
docker-compose build

echo "📦 Starting services..."
docker-compose up -d

echo "⏳ Waiting for database to be ready..."
sleep 10

echo "🗄️  Running migrations..."
docker-compose exec -T web python manage.py migrate

echo "📂 Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Services status:"
docker-compose ps

echo ""
echo "Next steps:"
echo "1. Create superuser: docker-compose exec web python manage.py createsuperuser"
echo "2. Check logs: docker-compose logs -f web"
echo "3. Visit your application at https://yourdomain.com"
echo "4. Admin panel: https://yourdomain.com/admin"
