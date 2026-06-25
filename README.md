# Snowball
Value Investment Assistant.

## Step 1. Document Retrieval 

### 1.1 Overview
Retrieve the past 6 years of 10k's, 10Q', Proxy Statements, and Earning Calls. Chunk and store these docuements for 
ease of use.

### 1.2 Pulling Documents
Documents will be pulled from EDGAR, specifically their HTML format variant for the structure that comes with it.

### 1.3 Chunking Documents
- **10-K's and 10-Q's**: Both of these documents follow standard orginization and can be split by Item headers in the HTML
- **Proxy statements**: These follow less structure but numbers can be grabbed using edgartools and the three main sections can be gotten via HTML headers

Following the chunking HTML tags will be removed for a clean text-only output.

### 1.4 Storing Documents
Documents will be cached in S3 so that re-retrieval will not be needed.
---
## Step 2. LLM Rankings

### 2.1 Overview
Feed into LLM to output a variety of rankings of various metrics based on readings.

---

## Step 3. Model Prediction
### 3.1 Overview
Feed variables from LLM into trained model to output predicted future free cash flow of company.
