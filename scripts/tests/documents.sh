#!/bin/bash
curl -N "http://localhost:8080/documents/AAPL" \
  -H "Content-Type: application/json" \
  -d '{"start_year": 2020, "end_year": 2025}'
