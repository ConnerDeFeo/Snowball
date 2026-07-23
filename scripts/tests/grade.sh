#!/bin/bash
curl -N "http://localhost:8080/grade_section/AAPL" \
  -H "Content-Type: application/json" \
  -d '{"start_year": 2020, "end_year": 2025, "rubric_category": "revenue_durability"}'
