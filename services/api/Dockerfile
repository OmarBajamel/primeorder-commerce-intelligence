FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATA_MODE=public-demo

WORKDIR /workspace

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY packages ./packages
COPY services ./services
COPY scripts ./scripts
COPY data ./data
COPY analytics ./analytics
COPY apps/web/public ./apps/web/public

RUN python scripts/generate_demo_data.py

EXPOSE 8000
CMD ["uvicorn", "services.api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
