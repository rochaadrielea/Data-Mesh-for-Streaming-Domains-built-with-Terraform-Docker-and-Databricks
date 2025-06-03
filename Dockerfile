# Use an official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command for testing
CMD ["python", "simulate_domain_cli.py", "--domain", "all"]
