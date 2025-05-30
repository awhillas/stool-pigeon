FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=pigeon.settings_k8s

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# # Create directory for SQLite database
# RUN mkdir -p /data/db
# RUN chmod 777 /data/db
# # Set the database path to persistent storage
# ENV SQLITE_PATH=/data/db/db.sqlite3

# Expose port
EXPOSE 3000

ENV DJANGO_SETTINGS_MODULE="pigeon.production" \
    DEBUG="true"

CMD python manage.py migrate && \
    python manage.py setup_site && \ 
    python manage.py collectstatic --noinput && \
    uvicorn pigeon.asgi:application --host 0.0.0.0 --port 3000
