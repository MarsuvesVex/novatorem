# Dockerfile
# syntax=docker/dockerfile:1
FROM python:3.10.0

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir

COPY api /app/api

ENV PYTHONPATH=/app
ENV PORT=5000

# Use the WSGI entry point consistently
CMD ["gunicorn", "--workers=2", "--bind", "0.0.0.0:5000", "api.wsgi:app"]
