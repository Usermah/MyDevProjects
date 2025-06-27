# Start with a base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system-level dependencies needed for pip packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libkrb5-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement files and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (optional)
RUN python manage.py collectstatic --noinput

# Set the port for gunicorn to run
EXPOSE 8000

# Start the Django app with Gunicorn
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
