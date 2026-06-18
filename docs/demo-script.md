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

