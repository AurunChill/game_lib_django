#!/bin/sh

# Run migrations
poertyr run python manage.py makemigrations --noinput
poetry run python manage.py migrate --noinput

# Create a superuser if it doesn't exist
poetry run python create_superuser.py

# Collect static files
poetry run python manage.py collectstatic --noinput

# Start the application
exec "$@"