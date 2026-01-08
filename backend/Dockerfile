# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app

# Install system dependencies (Tesseract OCR, Poppler for pdf2image)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy contents into a 'backend' directory to match the package structure
COPY . backend/

# Expose port 8000
EXPOSE 8000

# Run the application using the package path
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
