# Retail Ops Agent GCP — Handoff

**Updated:** June 18, 2026
**Purpose:** Context file so the next agent (Claude/Codex) can continue without the prior chat.

## Local Folder

This file lives at the root of the local checkout. Use `pwd` from this directory to see the machine-specific path.

## GitHub Location

```text
https://github.com/akhilesh12354/retail-ops-agent-gcp
```

## Why This Project Exists

Flagship GitHub portfolio project for Akhilesh Thokala's Google Cloud Customer Engineer / Platform Retail application. It makes the resume's "RetailOperationsAgent PoC on GCP" claim verifiable with public-safe synthetic data: Vertex/Gemini reasoning, BigQuery inventory truth layer, Cloud Run serving, phantom-inventory detection, BOPIS / ship-from-store routing, peak-season ops, refusal guardrails, source-grounded responses, and evals.

## Verified Current State (re-checked June 18, 2026)

Everything below was run and confirmed this session — not just claimed:

- `make test` → **10 tests passed**
- `make eval` → **4/4 evals passed** (phantom inventory, BOPIS route, peak-season throttle, guarantee refusal)
- `make demo` → grounded answers with source-row citations for all 5 scenarios
- GitHub Actions CI → **completed successfully** on push `27791106057`

The core test/eval/demo path runs fully local with Python **stdlib only**. Optional extras in `pyproject.toml` add FastAPI/Uvicorn and GCP clients without breaking the zero-dependency core path.

Implemented and working: synthetic inventory/order/capacity CSVs, phantom-inventory detection, BOPIS routing, peak-season throttling, refusal guardrails, grounded responses with citations, local demo, eval harness, unit tests, full docs set, MIT license, Mermaid README architecture, demo transcript, GitHub Actions CI config, optional FastAPI API path, BigQuery seed script, BigQuery repository adapter, and strict Vertex/Gemini tool-call validation boundary.

Cloud integration points are still **honest and opt-in**. BigQuery seeding/repository code is implemented but requires `pip install '.[gcp]'`, GCP auth, and a project. Gemini planning still raises `NotImplementedError` until live model wiring is intentionally added.

- `app/agent/vertex_adapter.py` — Vertex/Gemini tool-calling boundary with strict schema validation
- `app/services/bigquery_inventory.py` — BigQuery repository adapter, lazy-imported
- `scripts/seed_bigquery.py` — BigQuery seeding script with explicit schemas
- `app/api/main.py` — optional FastAPI app with stdlib fallback
- `infra/cloudrun.Dockerfile`, `infra/deploy.sh` — Cloud Run deploy scaffolding

## ⚠️ Steering Notes for the Next Agent — READ FIRST

1. **This is now pushed to GitHub.** Keep future work on `main` or short feature branches, and verify CI after every push.
2. **Codex's prior work is trustworthy and accurate** — claims in the old handoff matched reality on re-test. Keep that standard: only mark something done after running it.
3. **Do not fake cloud functionality.** The stubs are a feature. If you implement Vertex/BigQuery, make it genuinely work behind an env-gated flag; otherwise leave the honest `NotImplementedError` in place. Never claim production GCP that isn't running.
4. **Keep the repo runnable from a fresh clone with zero external deps** for the core demo/test/eval path. Any new dependency (FastAPI, google-cloud-*) must be optional and not break `make test/eval/demo`.

## Next Sprint — Prioritized, with Acceptance Criteria

**P0 — Make it a real portfolio repo (do first):**

1. Keep GitHub Actions green after every change. Acceptance: `make test` and `make eval` pass locally and in CI.
2. Add repo topics/description on GitHub if not already set. Suggested topics: `gcp`, `retail`, `bigquery`, `cloud-run`, `vertex-ai`, `gemini`, `bopis`, `inventory`, `agent`.
3. Add this repo to the GitHub profile README and pin it.

**P1 — Make the README portfolio-grade (cheap, high signal):**

4. Add screenshots or a terminal GIF only if useful. Mermaid diagram and demo transcript are already present.

**P2 — Real cloud, only if genuinely implemented (env-gated, optional deps):**

5. Cloud Run smoke-test notes added to `docs/gcp-deployment.md` after a real deploy.
6. Live Gemini planning if cloud credentials are available. Acceptance: deterministic planner stays the default; Gemini path is opt-in and validated before any tool executes.

## Commands

```bash
cd retail-ops-agent-gcp
make test   # 10 passing
make eval   # 4/4 passing
make demo   # grounded answers for 5 scenarios
```

## Demo Questions

1. Why is SKU-1842 showing available but failing pickup orders in Store 117?
2. Route this BOPIS order for ZIP 27701 with SLA under 2 hours.
3. We are entering Black Friday mode. Which stores should stop accepting ship-from-store orders?
4. Can you guarantee this item will be available tomorrow? (must refuse)
5. Show the evidence behind your routing decision.

## Important Files

```text
README.md                              Public project overview
Makefile                               test/eval/demo commands
app/agent/planner.py                   local deterministic planner
app/agent/guardrails.py                refusal rules
app/agent/tools.py                     tool wrapper used by planner
app/agent/citations.py                 source-row citation builder
app/services/anomaly_detection.py      phantom inventory logic
app/services/routing_engine.py         BOPIS / ship-from-store routing logic
app/services/inventory_repository.py   CSV-backed BigQuery-shaped repository
app/services/bigquery_inventory.py     optional BigQuery adapter
app/agent/vertex_adapter.py            strict Vertex/Gemini tool-call validation boundary
app/api/main.py                        optional FastAPI app with stdlib fallback
data/*.csv                             synthetic public-safe retail data
evals/run_evals.py                     eval runner
evals/eval_cases.json                  eval cases
infra/cloudrun.Dockerfile, deploy.sh   Cloud Run scaffolding
.github/workflows/ci.yml               GitHub Actions test/eval workflow
docs/                                  architecture, gcp-deployment, demo-script,
                                       demo-transcript, design-decisions,
                                       eval-methodology
```

## Safety Constraints (do not violate)

Do not add: real customer names, production inventory/order data, secrets/tokens/private endpoints, HIPAA/PCI/production-compliance claims unless actually implemented, or guarantees of future inventory availability. All public examples stay synthetic.
