FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Create data directory for TinyDB
RUN mkdir -p /data

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
