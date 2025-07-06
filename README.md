# Ebast - Django Web Application

A Django-based web application for managing various operational data and processes.

## Deployment Options

This application supports two deployment methods:

### 🐳 Docker Deployment (Recommended)

Docker provides a consistent, portable, and scalable deployment solution with built-in monitoring, security, and backup features.

**Quick Start:**
```bash
# Development
./deploy-dev.sh

# Production
./deploy.sh
```

**Benefits:**
- ✅ Consistent environment across development, testing, and production
- ✅ Built-in PostgreSQL, Nginx, and health monitoring
- ✅ Easy scaling and backup/recovery
- ✅ Security isolation and optimizations
- ✅ Automated SSL/HTTPS setup

**See:** [Docker Deployment Guide](DOCKER_DEPLOYMENT.md) for comprehensive instructions.

### 🔧 Traditional Git Pull Deployment

For simple deployments or when Docker is not available.

**Benefits:**
- ✅ Simple setup and direct file access
- ✅ Lower resource overhead
- ✅ Easy debugging and development

**See:** [Traditional Deployment Instructions](#traditional-deployment-instructions) below.

---

## Traditional Deployment Instructions

This guide will help you deploy the web application using Nginx and Gunicorn. All the necessary files are located in the `deployment` folder.

### Prerequisites

- Ensure you have Nginx installed on your server.
- Ensure you have Gunicorn installed. You can install it using pip:
  ```bash
  pip install gunicorn
  ```

### Step 1: Configure Nginx

1. Copy the Nginx configuration file to the appropriate directory:
   ```bash
   sudo cp /path/to/ebast/deployment/ebast /etc/nginx/sites-available/
   ```
   Modify the content accordingly

2. Create a symbolic link to enable the configuration:
   ```bash
   sudo ln -s /etc/nginx/sites-available/ebast /etc/nginx/sites-enabled/
   ```

3. Start the Nginx
   ```bash
   sudo systemctl start nginx
   ```

4. Test the Nginx configuration:
   ```bash
   sudo nginx -t
   ```

5. Reload Nginx to apply the changes:
   ```bash
   sudo systemctl reload nginx
   ```

### Step 2: Configure Gunicorn

1. Navigate to your project directory:
   ```bash
   cd /path/to/ebast
   ```

2. Start Gunicorn with your application:
   ```bash
   gunicorn --workers 3 --bind unix:/run/ebast.sock ebast.wsgi:application
   ```

### Step 3: Set Up Systemd Service for Gunicorn

1. Create a systemd service file for Gunicorn:
   ```bash
   sudo cp /path/to/ebast/deployment/ebast.service /etc/systemd/system/ebast.service
   ```
   change the `WorkingDirectory` and `ExecStart` accordingly

2. Start and enable the Gunicorn service:
   ```bash
   sudo systemctl start ebast.service
   sudo systemctl enable ebast.service
   ```

3. Check the status of the Gunicorn service:
   ```bash
   sudo systemctl status ebast.service
   ```

4. Check if the socket is working properly:
   ```bash
   curl --unix-socket /run/ebast.sock localhost
   ```

Ebast should now be deployed and accessible through Nginx and Gunicorn.

## Development Setup

### Prerequisites
- Python 3.10+
- pip
- virtualenv (recommended)

### Local Development
```bash
# Clone the repository
git clone https://github.com/ftharyanto/ebast.git
cd ebast

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Project Structure

```
ebast/
├── bast/                   # BAST module
├── cl_seiscomp/           # Seiscomp checklist module
├── core/                  # Core application
├── deployment/            # Traditional deployment files
├── qc/                    # Quality control module
├── qcfm/                  # QC FM module
├── text_format_converter/ # Text format converter
├── ebast/                 # Django project settings
├── static/                # Static files
├── media/                 # Media files
├── docker-compose.yml     # Docker production config
├── docker-compose.dev.yml # Docker development config
├── Dockerfile            # Docker image definition
├── nginx.conf            # Nginx configuration for Docker
├── deploy.sh             # Production deployment script
├── deploy-dev.sh         # Development deployment script
└── requirements.txt      # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.