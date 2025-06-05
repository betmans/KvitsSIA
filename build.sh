#!/usr/bin/env bash
# Exit on error
set -o errexit

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Populate products (TEMPORARY - REMOVE AFTER FIRST SUCCESSFUL IMPORT)
# echo "Attempting to import products..."
# python manage.py import_products
# echo "Product import command finished."

# Start Gunicorn
# Ensure Gunicorn is in your requirements.txt
# The PORT environment variable is automatically set by Cloud Run.
exec gunicorn kvits.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --worker-tmp-dir /dev/shm