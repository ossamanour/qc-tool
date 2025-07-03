FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpoppler-dev \
    poppler-utils \
    tesseract-ocr \
    libtesseract-dev \
    libpq-dev \
    postgresql-client \
    gcc \
    build-essential \
    pkg-config \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytesseract

# Expose Flask port
EXPOSE 5000

# Start Flask app
CMD ["python", "app.py"]