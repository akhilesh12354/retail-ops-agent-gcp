# GCP Deployment Plan

This repo is currently local-first. The intended Google Cloud deployment path is:

1. Load synthetic CSVs into BigQuery.
2. Deploy the API container to Cloud Run.
3. Grant the Cloud Run service account read-only access to the BigQuery dataset.
4. Configure Vertex AI / Gemini for bounded tool-calling.
5. Run smoke evals against the deployed endpoint.

For a complete sandbox checklist, see [native-gcp-validation.md](native-gcp-validation.md).

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

## Environment Variables configuration

To enable live GCP services on Cloud Run (or in local container tests), configure the following environment variables:

| Variable | Required | Default | Description |
|---|---|---|---|
| `USE_BIGQUERY` | Optional | `false` | Set to `true` to retrieve data from BigQuery instead of local CSVs. |
| `USE_VERTEX_AI` | Optional | `false` | Set to `true` to plan tool routing using live Vertex AI (Gemini). |
| `GOOGLE_CLOUD_PROJECT` | Required if either `true` | - | The Google Cloud project ID. |
| `BIGQUERY_DATASET` | Optional | `retail_ops_demo` | The BigQuery dataset containing the synthetic tables. |
| `VERTEX_LOCATION` | Optional | `us-central1` | The region where Vertex AI Gemini client is called. |
| `VERTEX_MODEL` | Optional | `gemini-2.5-flash` | The Gemini model name to query. |

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
docker run -p 8080:8080 \
  -e USE_BIGQUERY=true \
  -e USE_VERTEX_AI=true \
  -e GOOGLE_CLOUD_PROJECT=your-project-id \
  retail-ops-agent-gcp
```

## IAM Notes

Use a dedicated service account for Cloud Run:

- `roles/bigquery.dataViewer` on the demo dataset
- `roles/bigquery.jobUser` on the project
- `roles/aiplatform.user` on the project (required when live Vertex AI Gemini routing is enabled via `USE_VERTEX_AI=true`)

## Production Hardening Checklist

- Require authentication for non-demo deployments.
- Add request logging without customer PII.
- Add Cloud Monitoring dashboards for latency, refusal rate, and eval pass rate.
- Add rate limits or API Gateway/Apigee in front of public endpoints.
- Use Secret Manager for configuration.
