FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATA_MODE=public-demo

WORKDIR /workspace

COPY services/api/requirements.lock ./services/api/requirements.lock
RUN pip install --no-cache-dir --require-hashes -r services/api/requirements.lock

COPY packages ./packages
COPY services ./services
COPY data/public-demo ./data/public-demo

RUN useradd --create-home --uid 10001 appuser && chown -R appuser:appuser /workspace
USER appuser

EXPOSE 8000
CMD ["uvicorn", "services.api.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
