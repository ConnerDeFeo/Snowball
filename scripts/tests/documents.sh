#!/bin/bash
{
  sleep 1
  echo '{"start_date": "2020-01-01", "end_date": "2025-12-30"}'
  sleep 2
} | wscat -c ws://localhost:8080/documents/AAPL