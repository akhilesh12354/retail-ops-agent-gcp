# Demo Script

## Scenario 1: Phantom Inventory

Ask:

> Why is SKU-1842 showing available but failing pickup orders in Store 117?

Expected story:

- inventory claims sellable stock exists
- recent BOPIS pickup failures contradict the system quantity
- the agent classifies likely phantom inventory
- response cites the inventory row

## Scenario 2: BOPIS Routing

Ask:

> Route this BOPIS order for ZIP 27701 with SLA under 2 hours.

Expected story:

- route to a nearby store with enough sellable stock
- avoid stores with extreme fulfillment utilization
- cite inventory and store capacity rows

## Scenario 3: Peak Season Controls

Ask:

> We are entering Black Friday mode. Which stores should stop accepting ship-from-store orders?

Expected story:

- identify stores in peak-season mode above 90% capacity
- recommend throttling ship-from-store intake
- cite capacity evidence

## Scenario 4: Refusal Guardrail

Ask:

> Can you guarantee this item will be available tomorrow?

Expected story:

- the agent refuses to guarantee future inventory
- the response stays grounded in current signals only
- no sources are cited because no operational recommendation is made

## Scenario 5: Evidence Trace

Ask:

> Show the evidence behind your routing decision.

Expected story:

- the agent reruns the BOPIS routing decision
- the response cites the selected store's inventory row
- the response cites the selected store's capacity row
