# ----------------------------------------------------------
# Use a lightweight Python base image (Debian-based "slim")
# ----------------------------------------------------------
FROM python:3.11-slim

# Set environment variables and prevent python from writting .pyc files
ENV PYTHONDONTWRITTEBYTECODE=1

# No bufferring
ENV PYTHONBUFFERED=1


# Set the working directory inside the container
# All following commands (COPY, RUN, CMD, etc.) will be executed inside /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev curl git \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
# Copy the requirements.txt
COPY requirements.txt .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install all Python libraries listed in requirements.txt
RUN pip install -r requirements.txt

# Copy your Django project code into the container
# This copies the entire backend directory contents into /app
COPY . .


# Expose port 8000 to the host machine
# This tells Docker that the container will listen on port 8000.
EXPOSE 8000


# Set the default command to start the Django app using Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]