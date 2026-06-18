# Demo Transcript

Generated from:

```bash
make demo
```

## Phantom Inventory

**Q:** Why is SKU-1842 showing available but failing pickup orders in Store 117?

**A:** SKU-1842 at Store 117 shows 4 sellable units, but 2/3 recent pickup orders failed. Treat it as likely phantom inventory until a cycle count or store confirmation refreshes the inventory truth layer.

**Decision:** `likely_phantom_inventory`

**Evidence:** `data/sample_inventory.csv`, Store 117, SKU-1842, on hand 7, reserved 1, safety stock 2.

## BOPIS Routing

**Q:** Route this BOPIS order for ZIP 27701 with SLA under 2 hours.

**A:** Route BOPIS order for SKU-1842 to Store 118. It has 9 sellable units, is 23 miles from ZIP 27701, and is at 51% fulfillment utilization.

**Decision:** `route_selected`

**Evidence:** `data/sample_inventory.csv` and `data/sample_store_capacity.csv`.

## Peak Season Controls

**Q:** We are entering Black Friday mode. Which stores should stop accepting ship-from-store orders?

**A:** Stop or throttle ship-from-store intake for store(s) 117, 221; each is in peak-season mode above 90% fulfillment capacity.

**Decision:** `throttle_ship_from_store`

**Evidence:** `data/sample_store_capacity.csv`.

## Refusal Behavior

**Q:** Can you guarantee this item will be available tomorrow?

**A:** I cannot guarantee future inventory availability. I can only provide a grounded assessment from current inventory, order, and capacity signals.

**Decision:** `refused`
