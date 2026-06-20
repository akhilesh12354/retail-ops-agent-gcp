#!/usr/bin/env bash
set -euo pipefail

: "${GOOGLE_CLOUD_PROJECT:?Set GOOGLE_CLOUD_PROJECT first}"
: "${REGION:=us-central1}"
: "${USE_BIGQUERY:=false}"
: "${USE_VERTEX_AI:=false}"
: "${BIGQUERY_DATASET:=retail_ops_demo}"
: "${VERTEX_LOCATION:=us-central1}"
: "${VERTEX_MODEL:=gemini-2.5-flash}"

# NOTE: --allow-unauthenticated is for the public demo only. For any non-demo
# deployment, remove this flag and require authentication (see docs/gcp-deployment.md).
gcloud run deploy retail-ops-agent-gcp \
  --source . \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --region "$REGION" \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,USE_BIGQUERY=$USE_BIGQUERY,USE_VERTEX_AI=$USE_VERTEX_AI,BIGQUERY_DATASET=$BIGQUERY_DATASET,VERTEX_LOCATION=$VERTEX_LOCATION,VERTEX_MODEL=$VERTEX_MODEL" \
  --allow-unauthenticated
