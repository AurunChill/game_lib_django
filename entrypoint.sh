#!/bin/bash

# Run migrations
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create a superuser if it doesn't exist
python create_superuser.py

# Collect static files
python manage.py collectstatic --noinput

# Start the application
exec "$@"