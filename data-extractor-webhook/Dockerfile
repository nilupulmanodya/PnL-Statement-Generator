# Use an official lightweight Python image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies, ensuring gunicorn is installed globally
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy the application code
COPY . .

# Expose the port Flask will run on
EXPOSE 8080

# Ensure the correct working directory and command
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "webhook_listner:app"]
