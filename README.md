# Deployment Instructions

This guide will help you deploy the web application using Nginx and Gunicorn. All the necessary files are located in the `deployment` folder.

## Prerequisites

- Ensure you have Nginx installed on your server.
- Ensure you have Gunicorn installed. You can install it using pip:
  ```bash
  pip install gunicorn
  ```

## Step 1: Configure Nginx

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

## Step 2: Configure Gunicorn

1. Navigate to your project directory:
   ```bash
   cd /path/to/ebast
   ```

2. Start Gunicorn with your application:
   ```bash
   gunicorn --workers 3 --bind unix:/run/ebast.sock ebast.wsgi:application
   ```

## Step 3: Set Up Systemd Service for Gunicorn

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
   

ebast should now be deployed and accessible through Nginx and Gunicorn.