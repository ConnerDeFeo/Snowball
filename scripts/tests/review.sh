#!/bin/bash
curl -N http://localhost:8080/review/AAPL \
  -H "Content-Type: application/json" \
  -d '{"start_year": 2020, "end_year": 2025, "user_text": "Given that Apple deliberately does not disclose unbilled consideration for its long-term service arrangements, how should that blind spot affect confidence in the revenue durability grade of 62.0, and does the accelerating Services growth (+14% YoY, 75.4% margin) sufficiently offset the continued 50% revenue concentration in iPhone?"}'