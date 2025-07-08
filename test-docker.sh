#!/bin/bash

# Simple Docker test script
echo "🧪 Testing Docker setup..."

# Build the image
echo "🏗️  Building test image..."
docker-compose -f docker-compose.test.yml build

# Start the container
echo "🚀 Starting test container..."
docker-compose -f docker-compose.test.yml up -d

# Wait for container to be ready
echo "⏳ Waiting for container to be ready..."
sleep 30

# Test health check
echo "🩺 Testing health check..."
if curl -f http://localhost:8001/health/ > /dev/null 2>&1; then
    echo "✅ Health check passed!"
    health_check_passed=true
else
    echo "❌ Health check failed!"
    health_check_passed=false
fi

# Test home page
echo "🏠 Testing home page..."
if curl -f http://localhost:8001/ > /dev/null 2>&1; then
    echo "✅ Home page test passed!"
    home_page_passed=true
else
    echo "❌ Home page test failed!"
    home_page_passed=false
fi

# Show container logs
echo "📋 Container logs:"
docker-compose -f docker-compose.test.yml logs --tail=20

# Clean up
echo "🧹 Cleaning up..."
docker-compose -f docker-compose.test.yml down
docker rmi ebast-test 2>/dev/null || true

# Report results
echo ""
echo "📊 Test Results:"
if [ "$health_check_passed" = true ] && [ "$home_page_passed" = true ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed!"
    exit 1
fi