# Retail Discovery Questions

Google Cloud Customer Engineers need to qualify both the business pain and the technical path. These questions frame the demo as a realistic retail AI / data modernization pilot rather than a toy agent.

## Inventory Truth Layer

- What systems currently write inventory: POS, OMS, WMS, ERP, store handhelds, partner feeds?
- How often does store inventory sync to the enterprise inventory view?
- Which source wins when POS, OMS, and ERP disagree?
- How do you identify phantom inventory today: failed pickup, cycle counts, shrink, substitutions, customer complaints?
- What is the acceptable staleness window for BOPIS and ship-from-store decisions?

## Fulfillment And Routing

- What constraints decide BOPIS routing: distance, store capacity, labor, safety stock, SLA, margin, or customer tier?
- Do stores have separate capacity pools for pickup, ship-from-store, returns, and replenishment?
- What happens when the closest store is over capacity but has stock?
- How are substitutions, split shipments, and transfer orders handled?
- Which routing decisions require human approval during peak season?

## Peak Season Readiness

- What changes during Black Friday / holiday operations: safety stock, order cutoffs, capacity thresholds, carrier selection?
- Which systems have historically failed first under peak load?
- What are the RTO/RPO targets for inventory, checkout, fulfillment, and customer notifications?
- Which executive metrics are affected by downtime or inaccurate inventory?
- How are store/DC capacity changes communicated to digital channels?

## GCP Architecture Fit

- Which inventory and order datasets already live in BigQuery, Snowflake, Teradata, or an on-prem warehouse?
- Is the first pilot batch, streaming, or API-first?
- Would Cloud Run be enough for the serving layer, or are there GKE/runtime constraints?
- Does the agent need Vertex AI / Gemini, or would deterministic rules plus dashboards solve the first use case?
- What evidence must every AI answer cite before an operations team trusts it?

## Pilot Success Criteria

- Which decision should the pilot improve first: reduce failed pickups, improve SLA adherence, protect peak-season capacity, or reduce manual triage?
- What baseline metric exists today?
- What is the pilot scope: one region, one SKU family, one brand, or one fulfillment channel?
- What would convince store operations, ecommerce, and IT that the model is safe enough to expand?
- What data cannot leave the customer's environment?
