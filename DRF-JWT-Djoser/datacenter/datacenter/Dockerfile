# Base image: lightweight Python 3.12 slim image
FROM python:3.12-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Send Python output directly to terminal without buffering
ENV PYTHONUNBUFFERED 1

# Set working directory inside container to /app
WORKDIR /app

# Install gcc and Postgres libraries, then clean apt cache
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to container
COPY requirements.txt .

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Copy entrypoint.sh file into app container
COPY entrypoint.sh /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command: run Django development server on all interfaces port 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
