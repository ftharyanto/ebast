FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose Gunicorn port
EXPOSE 8000

# Run Gunicorn as the default command
CMD ["gunicorn", "ebast.wsgi:application"]
