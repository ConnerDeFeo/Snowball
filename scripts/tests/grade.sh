#!/bin/bash
wscat -c ws://localhost:8080/grade_section/AAPL \
  -x '{"start_date": "2020-01-01", "end_date": "2025-12-30", "rubric_category":"revenue_durability"}' \
  -w 30