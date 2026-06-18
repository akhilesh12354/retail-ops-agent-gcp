# Eval Methodology

The first eval suite checks decision correctness:

- phantom inventory classification
- BOPIS route selection
- peak-season throttling
- unsupported guarantee refusal

Future eval categories:

- grounding: every operational recommendation cites source rows
- routing quality: selected store satisfies stock, distance, capacity, and SLA constraints
- refusal behavior: unsupported forecasts and private-data requests are refused
- regression checks: changed routing logic does not break known scenarios

