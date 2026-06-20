# Native GCP Validation Plan

This repo is ready for a native Google Cloud smoke test after the local suite passes. Use a personal or approved sandbox project; do not use employer customer data, production endpoints, or private screenshots.

## Goal

Validate that the same retail-agent flow works with managed Google Cloud services:

- BigQuery as the inventory/order/capacity truth layer.
- Cloud Run as the serving boundary.
- Vertex AI / Gemini as the optional tool-call planner.
- Synthetic eval prompts as the smoke-test corpus.

## One-Time Project Setup

```bash
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com bigquery.googleapis.com aiplatform.googleapis.com cloudbuild.googleapis.com
```

Create or select a dedicated Cloud Run service account, then grant only the demo permissions:

```bash
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT" \
  --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:YOUR_SERVICE_ACCOUNT" \
  --role="roles/aiplatform.user"
```

Grant `roles/bigquery.dataViewer` at the dataset level after seeding the dataset.

## Validate BigQuery

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install '.[gcp]'

GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID \
BIGQUERY_DATASET=retail_ops_demo \
python scripts/seed_bigquery.py
```

Smoke check:

```bash
bq query --use_legacy_sql=false \
  'SELECT store_id, sku, on_hand FROM `YOUR_PROJECT_ID.retail_ops_demo.inventory` ORDER BY store_id LIMIT 5'
```

## Deploy Cloud Run

Start with deterministic local planning plus BigQuery:

```bash
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID \
USE_BIGQUERY=true \
USE_VERTEX_AI=false \
./infra/deploy.sh
```

Then test the service URL:

```bash
curl "$SERVICE_URL/health"
curl -X POST "$SERVICE_URL/query" \
  -H "Content-Type: application/json" \
  -d '{"question":"Route this BOPIS order for ZIP 27701 with SLA under 2 hours."}'
```

## Validate Vertex AI / Gemini Planning

After the BigQuery-backed path works, enable Gemini tool-call planning:

```bash
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID \
USE_BIGQUERY=true \
USE_VERTEX_AI=true \
VERTEX_LOCATION=us-central1 \
VERTEX_MODEL=gemini-2.5-flash \
./infra/deploy.sh
```

Run the same five demo prompts from the README and confirm:

- Unsupported guarantees are refused.
- Routing answers include source rows.
- Peak-season questions throttle overloaded stores.
- Cloud Run logs show no secret values or customer data.

## Push-Readiness Acceptance

Mark native GCP validation complete only after recording:

- Cloud Run service URL and deploy timestamp.
- BigQuery dataset/table names.
- Five prompt outputs with source citations.
- Any IAM deviations from the least-privilege notes above.
