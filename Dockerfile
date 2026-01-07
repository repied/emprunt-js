# Production Dockerfile for Google Cloud Run
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package in editable mode if needed, or just ensure src is in PYTHONPATH
ENV PYTHONPATH=/app/src

# Expose the port Cloud Run expects
EXPOSE $PORT

# Run the application
CMD ["sh", "-c", "uvicorn emprunt.app:app --host 0.0.0.0 --port $PORT"]
