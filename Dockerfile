# Use official Python image as base
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first for faster caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all 3 files (main.py, assignment.py, project.py) into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run GigHub using project.py as the entry point
CMD ["uvicorn", "project:app", "--host", "0.0.0.0", "--port", "8000"]