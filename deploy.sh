#!/bin/bash

# Docker Deployment Script for Production
# This script sets up and deploys the ebast application using Docker

set -e

echo "🚀 Starting Ebast Docker Deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.template .env
    echo "⚠️  Please edit .env file with your configuration before continuing."
    echo "🔧 Required changes:"
    echo "   - Set a secure SECRET_KEY"
    echo "   - Set a secure POSTGRES_PASSWORD"
    echo "   - Configure ALLOWED_HOSTS for your domain"
    echo ""
    echo "Run this script again after configuring .env file."
    exit 1
fi

# Check if environment variables are set
source .env

if [ "$SECRET_KEY" = "your-secret-key-here" ]; then
    echo "❌ Please set a secure SECRET_KEY in .env file"
    exit 1
fi

if [ "$POSTGRES_PASSWORD" = "your-secure-password-here" ]; then
    echo "❌ Please set a secure POSTGRES_PASSWORD in .env file"
    exit 1
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Build and start containers
echo "🏗️  Building Docker images..."
docker-compose build

echo "🔄 Starting containers..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 30

# Run migrations
echo "🔄 Running database migrations..."
docker-compose exec web python manage.py migrate

# Create superuser if needed
echo "👤 Creating superuser (if needed)..."
docker-compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Check container status
echo "📊 Checking container status..."
docker-compose ps

# Show logs
echo "📋 Recent logs:"
docker-compose logs --tail=10 web

echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Application is running at: http://localhost"
echo "🔐 Admin panel: http://localhost/admin"
echo "🩺 Health check: http://localhost/health"
echo ""
echo "📊 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart"