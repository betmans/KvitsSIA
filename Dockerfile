
# -----------------------------------------------------------------------------
# Stage 1: Build the application
# -----------------------------------------------------------------------------
FROM python:3.10-slim AS builder

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies (if any)
# RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
# Assumes requirements.txt is at the root of your repository
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

# Copy the entire project content from the repository root to /app in the image
# This assumes Dockerfile, manage.py, kvits/, kvitsapp/ are at the root.
COPY . /app/

# Collect static files using your main settings file
# Ensure STATIC_ROOT is correctly defined in kvits/settings.py
# This assumes manage.py is now at /app/manage.py
# Temporarily set DJANGO_DEBUG=True for collectstatic to avoid needing DATABASE_URL during build
RUN DJANGO_DEBUG=True python manage.py collectstatic --noinput --settings=kvits.settings
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

# Install runtime dependencies (if any)
# RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy the application code and collected static files from the builder stage
# This copies everything that was put into /app in the builder stage
COPY --from=builder /app/ /app/

# EXPOSE 8000 # Documentary, Cloud Run uses $PORT

# Run the application using Gunicorn
# Assumes kvits/wsgi.py is now at /app/kvits/wsgi.py
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:$PORT --workers ${GUNICORN_WORKERS:-2} --threads ${GUNICORN_THREADS:-4} --log-level info kvits.wsgi:application"]

