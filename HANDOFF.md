# Retail Ops Agent GCP - Handoff

**Updated:** June 20, 2026
**Purpose:** Continuation context for future local work on this portfolio repo.

## GitHub Location

```text
https://github.com/akhilesh12354/retail-ops-agent-gcp
```

## Current State

This is a public-safe, synthetic Google Cloud retail operations portfolio project. It supports the resume claim about a retail operations agent PoC on GCP using Vertex AI / Gemini, BigQuery, Cloud Run-style serving, BOPIS and ship-from-store routing, refusal guardrails, and source-grounded responses.

Verified locally on June 20, 2026:

- `make test` -> 24 tests passed
- `make eval` -> 42/42 eval scenarios passed
- Eval coverage spans six use cases: inventory detection, BOPIS routing, ship-from-store routing, peak-season controls, refusal guardrails, and source-grounded responses

## What Was Just Added

- Expanded eval coverage from 4 scenarios to 42 scenarios.
- Added optional BigQuery and Vertex AI / Gemini runtime configuration paths.
- Added live Vertex AI tool-call planning behind `USE_VERTEX_AI=true`; deterministic planning remains the default.
- Updated Cloud Run deployment env-var handling.
- Added `docs/native-gcp-validation.md` as the next-step test plan for a real GCP sandbox.
- Updated README claim mapping and public-safety language.

## Native GCP Next Step

Run the project in a sandbox GCP environment:

1. Enable Cloud Run, BigQuery, Vertex AI, and Cloud Build APIs.
2. Seed synthetic CSVs into BigQuery with `scripts/seed_bigquery.py`.
3. Deploy Cloud Run with `USE_BIGQUERY=true` and `USE_VERTEX_AI=false`.
4. Smoke test `/health` and `/query`.
5. Redeploy with `USE_VERTEX_AI=true` and verify Gemini tool-call planning.
6. Record prompt outputs, source citations, and IAM settings.

See `docs/native-gcp-validation.md` for the command-level checklist.

## Safety Constraints

- Do not add real customer names, customer diagrams, production inventory/order data, credentials, private endpoints, or screenshots from private systems.
- Keep `.env` untracked.
- Keep the local test/eval/demo path runnable without cloud credentials.
- Only claim production-grade GCP behavior after a real sandbox deployment has been performed and documented.

## Important Files

```text
README.md                              Public project overview and claim mapping
docs/native-gcp-validation.md          GCP sandbox validation checklist
docs/gcp-deployment.md                 Cloud Run / BigQuery / Vertex deployment notes
app/agent/planner.py                   deterministic planner plus optional Vertex adapter
app/agent/vertex_adapter.py            live Gemini tool-call adapter with validation
app/services/bigquery_inventory.py     optional BigQuery repository adapter
evals/eval_cases.json                  42 eval scenarios
evals/run_evals.py                     eval runner
infra/deploy.sh                        Cloud Run deploy script
```
