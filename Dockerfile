FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir "fastapi>=0.115.0" "uvicorn[standard]>=0.30.0" "google-cloud-bigquery>=3.25.0" "google-genai>=1.0.0"
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
