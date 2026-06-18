#!/usr/bin/env bash
set -euo pipefail

: "${GOOGLE_CLOUD_PROJECT:?Set GOOGLE_CLOUD_PROJECT first}"
: "${REGION:=us-central1}"

gcloud run deploy retail-ops-agent-gcp \
  --source . \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --region "$REGION" \
  --allow-unauthenticated

