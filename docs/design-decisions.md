# Design Decisions

## Deterministic Tools Before LLM Reasoning

The agent should not invent routing policy. Inventory math, capacity thresholds, and routing scores are implemented as normal code first. Gemini/Vertex should eventually translate operator questions into tool calls and summarize evidence.

## CSV Fallback Before BigQuery

The local CSV repository uses the same conceptual shape as the future BigQuery tables. This keeps the demo runnable without cloud credentials while preserving the architecture story.

## Refusal First

Guardrails run before tool execution. The public demo refuses unsupported guarantees, private-data requests, and unrelated regulated-advice questions.

## Deterministic Planner Scope

The local planner intentionally maps a small set of curated demo questions to bounded tool calls. It is not meant to be a general natural-language parser. That keeps the public demo deterministic, free to run, and easy to evaluate without live Gemini credentials.

The intended production shape is:

1. keep the deterministic tools as the source of truth
2. let Gemini select among those tools with a strict schema
3. validate every model-selected tool call before execution
4. fall back to the deterministic planner or a refusal when tool selection is unsupported
