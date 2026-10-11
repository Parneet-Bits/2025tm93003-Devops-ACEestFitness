# Small production image; test dependencies are isolated in the test target.
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    DATABASE_PATH=/app/data/aceest_fitness.db

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    && addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appgroup /app

COPY --chown=appuser:appgroup app.py ./app.py
COPY --chown=appuser:appgroup services.py ./services.py
COPY --chown=appuser:appgroup templates ./templates
COPY --chown=appuser:appgroup static ./static
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/healthz', timeout=2)" || exit 1
CMD ["python", "app.py"]

# CI builds this target to run the full test suite in an image derived from runtime.
FROM runtime AS test
USER root
COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt
COPY --chown=appuser:appgroup tests ./tests
ENV TESTING=1 DATABASE_PATH=/tmp/aceest-test.db
USER appuser
RUN python -m pytest -q
