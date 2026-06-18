# Design Decisions

## Deterministic Tools Before LLM Reasoning

The agent should not invent routing policy. Inventory math, capacity thresholds, and routing scores are implemented as normal code first. Gemini/Vertex should eventually translate operator questions into tool calls and summarize evidence.

## CSV Fallback Before BigQuery

The local CSV repository uses the same conceptual shape as the future BigQuery tables. This keeps the demo runnable without cloud credentials while preserving the architecture story.

## Refusal First

Guardrails run before tool execution. The public demo refuses unsupported guarantees, private-data requests, and unrelated regulated-advice questions.

