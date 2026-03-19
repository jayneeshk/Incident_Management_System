# FROM python:3.11

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY . .

# CMD ["python3", "app.py"]
# Use Python 3.11
# ===== Stage 1: Build stage =====
FROM python:3.11-slim AS builder

WORKDIR /app

# Install pipenv or dependencies
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# ===== Stage 2: Final image =====
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY --from=builder /app /app

# Expose Gunicorn port
EXPOSE 8000

# Run Gunicorn with 3 workers
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "app:app"]