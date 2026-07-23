#!/bin/bash
wscat -c ws://localhost:8080/documents/AAPL \
  -x '{"start_year": 2020, "end_year": 2025}' \
  -w 60