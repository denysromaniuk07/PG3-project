#!/bin/bash
# Django entrypoint script with database migrations and setup

set -e

echo "Starting Career Platform Backend..."

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z $DB_HOST ${DB_PORT:-5432}; do
  sleep 1
done
echo "Database is ready!"

# Wait for Redis to be ready
echo "Waiting for Redis..."
while ! nc -z $REDIS_HOST ${REDIS_PORT:-6379}; do
  sleep 1
done
echo "Redis is ready!"

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create cache table
echo "Creating cache table..."
python manage.py createcachetable

# Create superuser if it doesn't exist
echo "Setting up superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created successfully!")
else:
    print("Superuser 'admin' already exists!")
END

echo "Setup complete! Starting Gunicorn..."

# Start Gunicorn
exec gunicorn backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class sync \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  "$@"
