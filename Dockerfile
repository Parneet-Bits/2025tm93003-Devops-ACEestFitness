
# Stage 1: Base image
FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Testing image
FROM base AS test

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

ENV APP_VERSION=1.0.0

# Run tests with coverage
CMD ["pytest", "-v", "--cov=app", "--cov=services", "--cov-report=term-missing"]


# Stage 3: Production image
FROM base AS runtime

ARG APP_VERSION=1.0.0

ENV APP_VERSION=${APP_VERSION} \
    PORT=5000

# Create a non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Copy application files
COPY --chown=appuser:appgroup app.py services.py ./
COPY --chown=appuser:appgroup templates ./templates
COPY --chown=appuser:appgroup static ./static

# Create directory for SQLite database
RUN mkdir -p /app/instance && \
    chown -R appuser:appgroup /app/instance

USER appuser

EXPOSE 5000

# Container health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/healthz', timeout=3)" || exit 1

CMD ["python", "app.py"]
