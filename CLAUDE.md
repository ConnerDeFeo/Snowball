# Snowball — Project Context for Claude Code

## What this project is
Snowball is a proprietary system that predicts free cash flow (FCF) for public
equities by combining qualitative filing analysis (via LLM rubric scoring) with
a downstream statistical model. It's a personal research project, built as a
microservice architecture for both correctness and as a portfolio piece for
fintech/quant-adjacent recruiting.

## Pipeline (four steps)

1. **Document Retrieval** — Pull 6 years of 10-Ks, 10-Qs, proxy statements, and
   earnings calls from EDGAR (HTML format). Chunk by section. Cache in S3 so
   nothing is ever re-fetched unnecessarily.
2. **LLM Rankings** — Feed cached sections to an LLM, which scores the company
   across a fixed 10-category rubric (revenue durability, customer/supplier
   concentration, gross margin stability, moat/ROIC persistence, capital
   intensity, earnings quality, management/capital allocation, balance sheet
   resilience, industry structure, disclosure quality). Each score should be
   accompanied by structured reasoning/citations, not just a bare number —
   this is required for Step 4 to work later.
3. **Model Prediction** — Feed the Step 2 rubric outputs into a trained
   statistical model (scikit-learn) to predict forward FCF.
4. **Valuation Analysis** (future) — A LangChain agent that answers "why did
   the LLM score this the way it did," by dynamically pulling stored scores,
   reasoning, and raw filing sections to explain or audit a rating. This is
   an explainability/QA layer on the pipeline's own outputs, not a general
   chatbot.

## Architecture & language choices

| Concern | Tech | Why |
|---|---|---|
| Frontend | React TS + Tailwind | — |
| Orchestration / non-ML services | Go | Performance, concurrency, the stable backbone |
| Anything numerical, ML, or LLM-related | Python | Ecosystem maturity (Pydantic, edgartools, sklearn) |
| Containers | Docker | Microservice separation of concerns |
| Deployment | Kubernetes (EKS) + Terraform | Deliberate — partly a learning goal, not a load requirement |

**Services (2 containers now, a 3rd later):**
- `server` (Go) — entry point / main orchestrator for all Snowball calls.
  Handles pipeline coordination, scheduling, and concurrency.
- `analysis-pipeline` (Python) — a single container covering Steps 1–3, organized as
  internal modules/packages rather than separate services:
- `review-pipeline` (Python + LangChain, **future**, Step 4) — kept as its
  own separate service once built. Unlike Steps 1–3, this is *queried*
  on-demand rather than run as a sequential batch step, and could plausibly
  run interactively while a batch scoring job runs in the background
  elsewhere — a genuine reason to keep it independently deployable.

**Cross-cutting principles:**
- Step 2 (LLM scoring) is intentionally a deterministic pipeline (fixed input →
  fixed rubric → structured score), not agentic. LangChain does not belong
  there — use direct Bedrock calls + Pydantic schemas for structured output.
- K8s is not required by the pipeline's actual workload (it's closer to a
  batch job than a scaled service) — it's there deliberately for the learning
  value and deployment story. Don't over-architect Steps 1–3 around it.
- LangChain is reserved for Step 4 specifically, where dynamic, unpredictable
  tool use (deciding what to fetch based on intermediate results) is a
  genuine requirement — not for Steps 1–3.

---