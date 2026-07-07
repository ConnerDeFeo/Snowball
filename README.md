# Project Overview

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

### 2.2 Categories for rankings
The following are the categories

1. Revenue durability & quality — Recurring vs. transactional mix, contract length, organic vs. acquired growth, customer retention. Source: 10-K business section, segment footnotes, earnings call commentary on churn/backlog.
2. Customer & supplier concentration — Companies must disclose customers >10% of revenue in the 10-K. High concentration = fragile FCF. Also supplier dependence in risk factors.
3. Gross margin level & stability — High, stable gross margins are the single best proxy for pricing power. Trend over 5-10 years matters more than the level. (Novy-Marx showed gross profitability predicts returns better than earnings.)
4. Competitive moat / ROIC persistence — Does ROIC exceed cost of capital, and has the spread persisted or faded? Score the moat source: switching costs, network effects, cost advantage, intangibles. Source: your own ROIC calc from 10-Ks + qualitative reading.
5. Capital intensity & reinvestment burden — Capex/sales, capex/depreciation (rough maintenance vs. growth split), working capital as % of incremental revenue. Low-capital-intensity businesses convert earnings to FCF at much higher rates.
6. Earnings quality / cash conversion — Accruals ratio (net income minus CFO, scaled by assets), FCF/net income over time, growth in receivables or inventory outpacing revenue. This is the most directly predictive of future cash flow in the academic literature.
7. Management & capital allocation — This is where the proxy statement earns its keep: insider ownership, how incentive comp is structured (ROIC/FCF targets vs. raw EPS or revenue targets — huge tell), buyback timing vs. valuation, acquisition track record. Also candor in shareholder letters and earnings calls (do they own mistakes?).
8. Balance sheet resilience — Net debt/EBITDA, debt maturity ladder, off-balance-sheet obligations (leases, pensions, purchase commitments — all in footnotes). Leverage doesn't reduce FCF until it does, catastrophically.
9. Industry structure & cyclicality — End-market growth rate, competitive concentration, exposure to commodity inputs or macro cycles. A great company in a brutal industry has capped FCF durability.
10. Disclosure quality / accounting conservatism — Gap between GAAP and non-GAAP earnings, frequency of "one-time" charges, changes in accounting estimates, footnote opacity. This is a meta-signal: shady disclosure predicts shady cash flows.

---

## Step 3. Model Prediction
### 3.1 Overview
Feed variables from LLM into trained model to output predicted future free cash flow of company.

# Project Architecture

