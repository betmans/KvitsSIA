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

# Install system dependencies (if any are needed for your Python packages)
# Example for PostgreSQL client (psycopg2-binary usually handles this, but if not):
# RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc && rm -rf /var/lib/apt/lists/*
# Add any other build-time dependencies here.

# Copy requirements first to leverage Docker cache
COPY kvits.lv/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

# Copy the entire project structure from your 'kvits.lv' directory
# This assumes:
# - manage.py is at kvits.lv/manage.py
# - Your Django project 'kvits' (with settings.py, wsgi.py) is at kvits.lv/kvits/
# - Your Django app 'kvitsapp' is at kvits.lv/kvitsapp/
COPY kvits.lv/ /app/

# Collect static files using your main settings file
# Ensure STATIC_ROOT is correctly defined in kvits/settings.py
RUN python manage.py collectstatic --noinput --settings=kvits.settings
# The DJANGO_SETTINGS_MODULE will be set in the final stage for runtime.

# -----------------------------------------------------------------------------
# Stage 2: Production image
# -----------------------------------------------------------------------------
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# Set the DJANGO_SETTINGS_MODULE to your production settings file
ENV DJANGO_SETTINGS_MODULE=kvits.settings

# Install runtime dependencies (if any, e.g. libpq5 for psycopg2 if not using psycopg2-binary)
# RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy the application code and collected static files from the builder stage
COPY --from=builder /app/ /app/

# EXPOSE 8000 # This is documentary; Cloud Run uses $PORT. Gunicorn will use $PORT.

# Run the application using Gunicorn
# Ensure Gunicorn is in your requirements.txt
# The WSGI application path 'kvits.wsgi:application' should match your project structure.
# 'kvits' is your Django project directory inside /app (i.e., /app/kvits/wsgi.py)
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:$PORT --workers ${GUNICORN_WORKERS:-2} --threads ${GUNICORN_THREADS:-4} --log-level info kvits.wsgi:application"]
