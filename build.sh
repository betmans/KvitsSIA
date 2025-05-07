#!/usr/bin/env bash
# Exit on error
set -o errexit

# Collect static files
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Populate products (TEMPORARY - REMOVE AFTER FIRST SUCCESSFUL IMPORT)
echo "Attempting to import products..."
python manage.py import_products 
echo "Product import command finished."