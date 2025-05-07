FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create directory for static files
RUN mkdir -p kvitsapp/static/images

# Set permissions
RUN chmod -R 755 kvitsapp/static/images

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Restartē konteinerus
# docker-compose restart

# Visu novāc
# docker-compose down

# Visus failus izdzēš
# docker system prune -a --volumes

# Uzbūve no jauna
# docker-compose up --build

# Jaunās lietas migrē uz esošo dockeri
# docker-compose exec web python manage.py migrate

# Super admina izveide
# docker-compose exec web python manage.py createsuperuser

# Importē produktu katalogu
# docker-compose exec web python manage.py import_products

# Jāieliek pārlūkprogrammā lai apskatītu vietni
# http://localhost:8000/