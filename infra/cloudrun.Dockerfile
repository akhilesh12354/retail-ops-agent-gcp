FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir '.[api,gcp]'

ENV PYTHONUNBUFFERED=1
EXPOSE 8080

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
