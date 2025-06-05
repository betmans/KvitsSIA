# -----------------------------------------------------------------------------
# Stage 1: Build the application
# -----------------------------------------------------------------------------
FROM python:3.10-slim AS builder

# Set working directory
WORKDIR /app

# Set environment variables
# PYTHONUNBUFFERED ensures that Python output is sent straight to the terminal
# without being buffered first, which is good for logging.
ENV PYTHONUNBUFFERED 1
# PYTHONDONTWRITEBYTECODE prevents Python from writing .pyc files to disc.
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies (if any are needed for your Python packages, e.g., for Pillow or psycopg2)
# Example for PostgreSQL client (psycopg2-binary usually handles this, but if not):
# RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc && rm -rf /var/lib/apt/lists/*
# Add any other build-time dependencies here.

# Copy requirements first to leverage Docker cache
COPY kvits.lv/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

# Copy the entire project
# Assuming your Django project is within the 'kvits.lv' directory structure
# and your manage.py is at 'kvits.lv/manage.py'
# and your main Django project directory (with settings.py) is 'kvits.lv/kvits/'
# and your app is 'kvits.lv/kvitsapp/'
COPY kvits.lv/ /app/

# Collect static files
# This will use your settings_g.py if DJANGO_SETTINGS_MODULE is set,
# or you can specify it directly.
# Ensure STATIC_ROOT is correctly defined in settings_g.py
# Example: ENV DJANGO_SETTINGS_MODULE=kvits.settings_g
RUN python manage.py collectstatic --noinput --settings=kvits.settings_g
# If your manage.py is directly in /app (as copied above), and kvits.settings_g is the correct path:
# RUN DJANGO_SETTINGS_MODULE=kvits.settings_g python manage.py collectstatic --noinput

# -----------------------------------------------------------------------------
# Stage 2: Production image
# -----------------------------------------------------------------------------
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# Set the DJANGO_SETTINGS_MODULE to your production settings file for Google Cloud
ENV DJANGO_SETTINGS_MODULE=kvits.settings_g

# Install runtime dependencies (if any, e.g. libpq for postgres)
# RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy the application code and collected static files from the builder stage
COPY --from=builder /app/ /app/

# Expose the port the app runs on.
# Cloud Run automatically provides the PORT environment variable.
# Gunicorn will bind to this $PORT.
EXPOSE 8000 # Or whatever port $PORT will be, Gunicorn will use $PORT

# Run the application using Gunicorn
# Ensure Gunicorn is in your requirements.txt
# The WSGI application path 'kvits.wsgi:application' should match your project structure.
# 'kvits.wsgi' refers to kvits/wsgi.py
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --log-level info kvits.wsgi:application