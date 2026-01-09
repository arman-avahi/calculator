# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file if it exists
COPY requirements.txt* ./

# Install dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Run the Python application
CMD ["python", "main.py"]