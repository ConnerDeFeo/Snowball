#!/bin/bash
wscat -c ws://localhost:8080/grade_section/AAPL \
  -x '{"start_year": 2020, "end_year": 2025, "rubric_category":"revenue_durability"}' \
  -w 60