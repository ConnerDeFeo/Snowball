#!/bin/bash
curl -X POST http://localhost:8080/review/AAPL \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2020-01-01", "end_date": "2025-12-30", "user_text": "Given that Apple deliberately does not disclose unbilled consideration for its long-term service arrangements, how should that blind spot affect confidence in the revenue durability grade of 62.0, and does the accelerating Services growth (+14% YoY, 75.4% margin) sufficiently offset the continued 50% revenue concentration in iPhone?"}'