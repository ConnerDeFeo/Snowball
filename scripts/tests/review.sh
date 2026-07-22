#!/bin/bash
curl -X POST http://localhost:8080/review/AAPL \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2020-01-01", "end_date": "2025-12-30"}'