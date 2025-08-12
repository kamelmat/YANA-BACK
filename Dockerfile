# Use Python slim image directly (simpler than distroless)
FROM python:3.11.12-slim
WORKDIR /app

# Install system dependencies for psycopg2 (build and runtime)
RUN apt-get update && apt-get install -y \
  libpq5 \
  libpq-dev \
  gcc \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  rm -rf /root/.cache/pip

# Remove build dependencies to reduce image size
RUN apt-get update && apt-get remove -y \
  libpq-dev \
  gcc \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY yana/. yana/
COPY .github/scripts/start.py start.py

# Create non-root user
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1 \
  PORT=8000 \
  PYTHONPATH=/app:/app/yana

EXPOSE 8000

CMD ["/app/start.py"]