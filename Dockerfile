# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (e.g., for compiling libraries like Pillow)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY start.sh /start.sh
RUN chmod +x /start.sh

# Copy the current directory contents into the container at /app
COPY . /app/

# Set environment variables (optional but useful)
ENV PYTHONUNBUFFERED 1

# Expose the port the app will run on
EXPOSE 8000

# Run Django development server (or adjust to your entrypoint)
# Use Gunicorn to run the Django app in production
CMD ["gunicorn", "blogproj.wsgi:application", "--bind", "0.0.0.0:8000"]
