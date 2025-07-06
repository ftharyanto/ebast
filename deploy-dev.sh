#!/bin/bash

# Docker Development Deployment Script
# This script sets up and deploys the ebast application using Docker for development

set -e

echo "🚀 Starting Ebast Docker Development Environment..."

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

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.dev.yml down 2>/dev/null || true

# Build and start containers
echo "🏗️  Building Docker images..."
docker-compose -f docker-compose.dev.yml build

echo "🔄 Starting development containers..."
docker-compose -f docker-compose.dev.yml up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 30

# Run migrations
echo "🔄 Running database migrations..."
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate

# Create superuser if needed
echo "👤 Creating superuser (if needed)..."
docker-compose -f docker-compose.dev.yml exec web python manage.py shell -c "
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
docker-compose -f docker-compose.dev.yml ps

# Show logs
echo "📋 Recent logs:"
docker-compose -f docker-compose.dev.yml logs --tail=10 web

echo "✅ Development environment setup completed successfully!"
echo ""
echo "🌐 Application is running at: http://localhost:8000"
echo "🔐 Admin panel: http://localhost:8000/admin"
echo "🩺 Health check: http://localhost:8000/health"
echo "🗄️  Database: localhost:5432 (ebast_dev/ebast/ebast_password)"
echo ""
echo "📊 To view logs: docker-compose -f docker-compose.dev.yml logs -f"
echo "🛑 To stop: docker-compose -f docker-compose.dev.yml down"
echo "🔄 To restart: docker-compose -f docker-compose.dev.yml restart"