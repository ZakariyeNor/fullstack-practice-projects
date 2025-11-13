#!/bin/sh
set -e

# Make migrations only for the users app first
echo "Running makemigrations for users app..."
python manage.py makemigrations users

# Apply migrations for users app first
echo "Applying migrations for users app..."
python manage.py migrate users

# Then run migrations for all other apps
echo "Applying migrations for all other apps..."
python manage.py migrate

# Print a message before starting the server
echo "Starting Django development server..."
exec "$@"
