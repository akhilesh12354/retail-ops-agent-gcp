# Architecture

## Local MVP

The local MVP keeps the core deterministic:

- CSV-backed inventory repository
- routing and anomaly-detection services
- local planner that maps demo questions to tools
- guardrails before tool execution
- eval runner that checks expected decisions

This avoids the common AI-demo failure mode where the LLM is asked to compensate for missing business logic.

## Target GCP Shape

```text
Cloud Run API
  |
  +-- Vertex AI / Gemini tool-calling planner
  |
  +-- BigQuery inventory truth layer
  |
  +-- retail operations tools
      |-- phantom inventory detection
      |-- BOPIS routing
      |-- ship-from-store routing
      +-- peak-season capacity policy
```

## Why These Services

- **BigQuery:** central inventory and operations truth layer for large analytical joins.
- **Vertex AI / Gemini:** natural-language operator interface over bounded tools.
- **Cloud Run:** simple serverless API boundary with scale-to-zero and burst handling.

