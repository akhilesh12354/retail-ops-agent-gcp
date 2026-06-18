# GCP Deployment Plan

This repo is currently local-first. The intended Google Cloud deployment path is:

1. Load synthetic CSVs into BigQuery.
2. Deploy the API container to Cloud Run.
3. Grant the Cloud Run service account read-only access to the BigQuery dataset.
4. Configure Vertex AI / Gemini for bounded tool-calling.
5. Run smoke evals against the deployed endpoint.

## BigQuery Tables

Dataset: `retail_ops_demo`

| Table | Source | Purpose |
|---|---|---|
| `inventory` | `data/sample_inventory.csv` | Store/SKU stock and distance signals |
| `orders` | `data/sample_orders.csv` | Recent fulfillment outcomes |
| `store_capacity` | `data/sample_store_capacity.csv` | Fulfillment capacity and peak-season mode |

Seed command:

```bash
pip install '.[gcp]'
GOOGLE_CLOUD_PROJECT=your-project-id python scripts/seed_bigquery.py
```

## Cloud Run

The local service exposes:

- `GET /health`
- `POST /query` with `{"question": "..."}`

Build/deploy target:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id ./infra/deploy.sh
```

Local container target:

```bash
docker build -f infra/cloudrun.Dockerfile -t retail-ops-agent-gcp .
docker run -p 8080:8080 retail-ops-agent-gcp
```

## IAM Notes

Use a dedicated service account for Cloud Run:

- `roles/bigquery.dataViewer` on the demo dataset
- `roles/bigquery.jobUser` on the project
- Vertex AI permissions only when the Gemini adapter is enabled

## Production Hardening Checklist

- Require authentication for non-demo deployments.
- Add request logging without customer PII.
- Add Cloud Monitoring dashboards for latency, refusal rate, and eval pass rate.
- Add rate limits or API Gateway/Apigee in front of public endpoints.
- Use Secret Manager for configuration.
