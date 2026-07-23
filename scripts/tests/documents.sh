#!/bin/bash
{
  sleep 1
  echo '{"start_year": 2020, "end_year": 2025}'
  sleep 2
} | wscat -c ws://localhost:8080/documents/AAPL