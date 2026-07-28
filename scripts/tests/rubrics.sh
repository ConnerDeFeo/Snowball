#!/bin/bash
curl -X POST http://localhost:8080/rubric/revenue_durability \
  -H "Content-Type: application/json" \
  -d '{"name": "Revenue durability", "directions": "Determine what share of revenue is contractual, recurring, or subscription-based versus one-time or project-based, and how much visibility management has into future revenue (backlog, deferred revenue, remaining performance obligations)."}' \
  -w '\n'

curl -X POST http://localhost:8080/rubric/revenue_quality \
  -H "Content-Type: application/json" \
  -d '{"name": "Revenue quality", "directions": "Assess whether reported revenue reflects real cash-backed demand versus aggressive recognition timing, non-recurring gains, or channel-stuffing, using the recognition footnote and any MD&A caveats."}' \
  -w '\n'

curl -X POST http://localhost:8080/rubric/revenue_durability/sub_agent \
  -H "Content-Type: application/json" \
  -d '{"form": "10-K", "section": "part_i_item_1", "prompt": "Look for contract structure, recurring vs. project-based revenue, and backlog figures."}' \
  -w '\n'

curl -X POST http://localhost:8080/rubric/revenue_durability/sub_agent \
  -H "Content-Type: application/json" \
  -d '{"form": "10-K", "section": "part_ii_item_7", "prompt": "Look for management'"'"'s discussion of revenue drivers and disaggregation."}' \
  -w '\n'

curl -X POST http://localhost:8080/rubric/revenue_durability/sub_agent \
  -H "Content-Type: application/json" \
  -d '{"form": "10-K", "section": "part_ii_item_8", "prompt": "Look for the Revenue Recognition footnote, including ASC 606 disaggregation and remaining performance obligations."}' \
  -w '\n'

curl -X POST http://localhost:8080/rubric/revenue_quality/sub_agent \
  -H "Content-Type: application/json" \
  -d '{"form": "10-K", "section": "part_ii_item_7", "prompt": "Look for discussion of one-time items, divestiture gains, or channel-stuffing risk."}' \
  -w '\n'

curl -X POST http://localhost:8080/rubric/revenue_quality/sub_agent \
  -H "Content-Type: application/json" \
  -d '{"form": "10-K", "section": "part_ii_item_8", "prompt": "Look for the Revenue Recognition footnote'"'"'s detail on timing of recognition and contract assets/liabilities."}' \
  -w '\n'

# curl -X POST http://localhost:8080/rubric/revenue_quality/sub_agent \
#   -H "Content-Type: application/json" \
#   -d '{"form": "10-Q", "section": "part_i_item_1", "prompt": "Look for quarter-over-quarter revenue trend and any restatements in the financial statements."}' \
#   -w '\n'

# curl -X POST http://localhost:8080/rubric/revenue_quality/sub_agent \
#   -H "Content-Type: application/json" \
#   -d '{"form": "10-Q", "section": "part_i_item_2", "prompt": "Look for quarterly MD&A commentary on revenue trend."}' \
#   -w '\n'
