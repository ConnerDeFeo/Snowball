# Project Overview

## Step 1. Document Retrieval 

### 1.1 Overview
Retrieve the past 6 years of 10k's, 10Q', Proxy Statements, and Earning Calls. Chunk and store these docuements for 
ease of use.

### 1.2 Pulling Documents
Documents will be pulled from EDGAR, specifically their HTML format variant for the structure that comes with it.

### 1.3 Chunking Documents
Edgar tools will be used in python

### 1.4 Storing Documents
Documents will be cached in S3 so that re-retrieval will not be needed.
---
## Step 2. LLM Rankings

### 2.1 Overview
Feed into LLM to output a variety of rankings of various metrics based on readings.

### 2.2 Categories for rankings
The following are the categories

1. Revenue durability & quality
2. Customer & supplier concentration
3. Gross margin level & stability
4. Competitive moat / ROIC persistence
5. Capital intensity & reinvestment burden
6. Earnings quality / cash conversion
7. Management & capital allocation
8. Balance sheet resilience
9. Industry structure & cyclicality
10. Disclosure quality / accounting conservatism

---

## Step 3. Model Prediction
### 3.1 Overview
Feed variables from LLM into trained model to output predicted future free cash flow of company.

## Step 4. Valuation Analysis
This is the final step, use langchain to see the "why" behind all of the AI's scores.

# Project Architecture
The following are the containers for the application

### Server (Go)
Entry point for all main calls to snowball, main orchestrater

### Edgar Retrival (Python + Edgartools)
Grab documents and cache them section by section

### LLM (Python)
Generates rubric using LLM and sections handed to it

### Statistical Analysis (Python + Scikit-learn)
Python based backend ustalizing sckite-learn to deal with the graded rubrics