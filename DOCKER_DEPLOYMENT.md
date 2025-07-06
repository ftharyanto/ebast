# Docker Deployment Guide

This guide provides comprehensive instructions for deploying the Ebast application using Docker. Docker provides a consistent, portable, and scalable deployment solution.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Development Setup](#development-setup)
4. [Production Deployment](#production-deployment)
5. [Configuration](#configuration)
6. [Database Setup](#database-setup)
7. [SSL/HTTPS Setup](#ssl-https-setup)
8. [Monitoring and Logging](#monitoring-and-logging)
9. [Backup and Recovery](#backup-and-recovery)
10. [Troubleshooting](#troubleshooting)
11. [Migration from Git Pull Deployment](#migration-from-git-pull-deployment)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 1.29+
- At least 2GB RAM
- At least 10GB disk space

### Installing Docker

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**CentOS/RHEL:**
```bash
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

**Docker Compose:**
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/ftharyanto/ebast.git
cd ebast
```

### 2. Development Setup (Recommended for Testing)
```bash
./deploy-dev.sh
```

### 3. Production Deployment
```bash
./deploy.sh
```

## Development Setup

The development setup uses SQLite and runs Django's development server with hot reloading.

### Starting Development Environment
```bash
docker-compose -f docker-compose.dev.yml up -d
```

### Accessing the Application
- **Web Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin (admin/admin123)
- **Database**: localhost:5432
- **Health Check**: http://localhost:8000/health

### Development Commands
```bash
# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Run Django management commands
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
docker-compose -f docker-compose.dev.yml exec web python manage.py collectstatic

# Access Django shell
docker-compose -f docker-compose.dev.yml exec web python manage.py shell

# Stop development environment
docker-compose -f docker-compose.dev.yml down
```

## Production Deployment

The production setup uses PostgreSQL, Nginx, and Gunicorn with security optimizations.

### 1. Configuration

Create your environment file:
```bash
cp .env.template .env
```

Edit `.env` with your configuration:
```env
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=false
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
POSTGRES_PASSWORD=your-secure-database-password
```

### 2. Deploy
```bash
./deploy.sh
```

### 3. Accessing the Application
- **Web Application**: http://localhost (port 80)
- **Admin Panel**: http://localhost/admin
- **Health Check**: http://localhost/health

### Production Commands
```bash
# View logs
docker-compose logs -f

# Scale web application
docker-compose up -d --scale web=3

# Update application
git pull
docker-compose build
docker-compose up -d

# Backup database
docker-compose exec db pg_dump -U ebast ebast > backup.sql

# Restore database
docker-compose exec -T db psql -U ebast -d ebast < backup.sql
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | - | Yes |
| `DEBUG` | Debug mode | `false` | No |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` | No |
| `POSTGRES_DB` | Database name | `ebast` | No |
| `POSTGRES_USER` | Database user | `ebast` | No |
| `POSTGRES_PASSWORD` | Database password | - | Yes |
| `POSTGRES_HOST` | Database host | `db` | No |
| `POSTGRES_PORT` | Database port | `5432` | No |
| `HTTPS` | Enable HTTPS security | `false` | No |

### Custom Settings

Create a custom settings file by copying `ebast/settings_docker.py` and modifying it:
```python
# ebast/settings_custom.py
from .settings_docker import *

# Your custom settings
TIME_ZONE = 'Your/Timezone'
LANGUAGE_CODE = 'your-language'
```

Then update your environment:
```env
DJANGO_SETTINGS_MODULE=ebast.settings_custom
```

## Database Setup

### PostgreSQL (Recommended for Production)

The production setup automatically uses PostgreSQL. Data is persisted in Docker volumes.

### SQLite (Development Only)

Used automatically in development mode.

### Database Migration

```bash
# Create new migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## SSL/HTTPS Setup

### 1. Generate SSL Certificates

Create SSL certificates directory:
```bash
mkdir ssl
```

**Using Let's Encrypt:**
```bash
docker run -it --rm \
  -v $(pwd)/ssl:/etc/letsencrypt \
  -p 80:80 \
  certbot/certbot certonly --standalone \
  -d yourdomain.com
```

**Using Self-Signed Certificates (Development):**
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/privkey.pem \
  -out ssl/fullchain.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

### 2. Update Nginx Configuration

Edit `nginx.conf` to add SSL configuration:
```nginx
server {
    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    # ... rest of configuration
}
```

### 3. Update Environment

```env
HTTPS=true
```

## Monitoring and Logging

### Health Checks

All services include health checks:
- **Web**: http://localhost/health
- **Database**: PostgreSQL `pg_isready`
- **Nginx**: HTTP response check

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx

# Application logs
docker-compose exec web tail -f /app/logs/django.log
```

### Log Management

Logs are stored in:
- Container logs: `docker-compose logs`
- Application logs: `/app/logs/django.log` (inside container)
- Nginx logs: `/var/log/nginx/` (inside nginx container)

## Backup and Recovery

### Database Backup

```bash
# Create backup
docker-compose exec db pg_dump -U ebast ebast > backup_$(date +%Y%m%d_%H%M%S).sql

# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR
docker-compose exec db pg_dump -U ebast ebast > $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

### Media Files Backup

```bash
# Backup media files
docker run --rm -v ebast_media_volume:/data -v $(pwd)/backup:/backup alpine \
  tar czf /backup/media_backup_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
```

### Full Restore

```bash
# Restore database
docker-compose exec -T db psql -U ebast -d ebast < backup.sql

# Restore media files
docker run --rm -v ebast_media_volume:/data -v $(pwd)/backup:/backup alpine \
  tar xzf /backup/media_backup.tar.gz -C /data
```

## Troubleshooting

### Common Issues

**Container Won't Start:**
```bash
# Check logs
docker-compose logs web

# Check container status
docker-compose ps

# Rebuild container
docker-compose build --no-cache web
```

**Database Connection Issues:**
```bash
# Check database health
docker-compose exec db pg_isready -U ebast

# Check database logs
docker-compose logs db

# Reset database
docker-compose down
docker volume rm ebast_postgres_data
docker-compose up -d
```

**Permission Issues:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

**Out of Disk Space:**
```bash
# Clean up Docker
docker system prune -a
docker volume prune
```

### Performance Optimization

**Increase Resources:**
```yaml
# docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

**Scale Application:**
```bash
# Run multiple web containers
docker-compose up -d --scale web=3
```

## Migration from Git Pull Deployment

### 1. Backup Current Deployment

```bash
# Backup database
sudo -u postgres pg_dump ebast > ebast_backup.sql

# Backup media files
tar czf media_backup.tar.gz /path/to/ebast/media/

# Backup configuration
cp /etc/nginx/sites-available/ebast nginx_backup.conf
cp /etc/systemd/system/ebast.service systemd_backup.service
```

### 2. Stop Current Services

```bash
sudo systemctl stop ebast
sudo systemctl stop nginx
```

### 3. Deploy with Docker

```bash
# Setup Docker deployment
git clone https://github.com/ftharyanto/ebast.git ebast-docker
cd ebast-docker
cp .env.template .env
# Edit .env with your configuration
./deploy.sh
```

### 4. Migrate Data

```bash
# Restore database
docker-compose exec -T db psql -U ebast -d ebast < ebast_backup.sql

# Restore media files
docker run --rm -v ebast_media_volume:/data -v $(pwd):/backup alpine \
  tar xzf /backup/media_backup.tar.gz -C /data
```

### 5. Update DNS/Proxy

Update your reverse proxy or DNS to point to the Docker containers.

## Comparison: Docker vs Git Pull

| Feature | Docker Deployment | Git Pull Deployment |
|---------|-------------------|---------------------|
| **Environment Consistency** | ✅ Identical across environments | ❌ Environment-specific issues |
| **Dependency Management** | ✅ Containerized dependencies | ❌ Manual dependency management |
| **Scalability** | ✅ Easy horizontal scaling | ❌ Limited scalability |
| **Isolation** | ✅ Complete application isolation | ❌ Shared system resources |
| **Rollback** | ✅ Easy rollback with image tags | ❌ Manual git rollback |
| **Security** | ✅ Isolated security context | ❌ Direct system access |
| **Monitoring** | ✅ Built-in health checks | ❌ Manual monitoring setup |
| **Backup/Recovery** | ✅ Volume-based backups | ❌ Manual backup procedures |
| **Setup Complexity** | ❌ Initial learning curve | ✅ Simple setup |
| **Resource Usage** | ❌ Container overhead | ✅ Direct resource usage |
| **Debugging** | ❌ Container-based debugging | ✅ Direct file access |

## Best Practices

1. **Use specific image tags** in production
2. **Implement proper logging** and monitoring
3. **Regular backups** of database and media files
4. **Use secrets management** for sensitive data
5. **Implement proper health checks**
6. **Use reverse proxy** for SSL termination
7. **Monitor resource usage** and scale accordingly
8. **Test deployments** in staging environment first

## Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review Docker and Django documentation

## License

This deployment guide is part of the Ebast project. Please refer to the main project license.