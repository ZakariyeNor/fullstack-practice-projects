#!/bin/sh

# Exit immediately if a command fails
set -e

# Make migrations only for the users app first
echo "Running makemigrations for accounts app..."
python3 manage.py makemigrations accounts --noinput

# Apply migrations for users app first
echo "Applying migrations for accounts app..."
python3 manage.py migrate accounts --noinput

# Migrate
echo "Applying migrations..."
python3 manage.py migrate --noinput

echo "Migration completed"

# Execute the CMD from Dockerfile
exec "$@"
