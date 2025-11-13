#!/bin/sh

# Exit immediately if a command fails
set -e

# Make migrations only for the users app first
echo "Running makemigrations for users app..."
python3 manage.py makemigrations users

# Apply migrations for users app first
echo "Applying migrations for users app..."
python3 manage.py migrate users

# Migrate
echo "Applying migrations for all other apps..."
python3 manage.py migrate


echo "Applying migrations..."
python3 manage.py migrate

echo "Migrations complete"

# Execute the CMD from Dockerfile
exec "$@"
