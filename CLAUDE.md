# Snowball — CLAUDE.md

## What this is
Quantitative company-scoring system. It fetches public company documents (SEC
filings), analyzes and grades them across FCF-predictive categories, scores
them, and supports Q&A over the analysis. Three containers sit behind a Go
orchestrator.

## Architecture
Three containers:

1. **Go orchestrator** — entrypoint and routing; connects to the other two services.
2. **Analysis pipeline** — fetches → analyzes → grades → scores company documents.
3. **LangChain review pipeline** — answers specific questions about the analysis.
   <!-- TODO: describe exactly what this takes as input and returns -->

### Go orchestrator layout
- `cmd/orchestrator/main.go` — main entrypoint
- `internal/api/` — **generic** HTTP routing shared across everything
- `internal/analysis-pipeline/` — client/logic specific to the analysis pipeline container
- `internal/review-pipeline/` — client/logic specific to the review pipeline container

Rule of thumb: `internal/api/` stays generic. Anything specific to a downstream
container lives in that container's folder, not in `api/`.

### Analysis pipeline layout
- `document_retrieval/` — fetches public company documents; calls `utils/` to cache them to S3
- `utils/` — shared helpers (S3 caching, etc.)
- `routes/` — HTTP route handlers

## Infrastructure
- **Region:** AWS us-east-2
- **S3** — document / blob storage
- **DynamoDB** — metadata and scores
- **ECR** — container image registry (login + push scripts in `/scripts/`)
- **Terraform** — all infra defined in `terraform/` at repo root

## How to run / build / deploy
- **Local dev stack:** `docker compose up` (from repo root)
- **Prod stack:** `docker compose -f docker-compose.prod.yml up`
- **ECR login + image push:** scripts in `/scripts/`

Current workflow: I'm **not running this locally** right now — it's faster to build,
push images to ECR, and run them on an EC2 instance in AWS. Assume changes get
verified by deploying, not by a local run, unless I say otherwise.

## Tests
No tests yet — this is an early, move-fast build, not production-grade. Do **not**
add tests, CI, or test scaffolding unless I ask for it.

## Coding conventions
- **Keep files small.** Hard cap ~150 lines per file. If a file grows past that, split it.
- **Highly modular.** One clear responsibility per file/module. Prefer small, composable functions.
- **No over-engineering.** Build for the problem in front of you, not hypothetical ones.
  No speculative abstractions, no "maybe we'll need it" flexibility, no config or
  layers I didn't ask for. Reach for the stdlib / native capability before adding a dependency.
- **Simplicity beats cleverness.** The shortest solution that actually works wins.

## How to work with me
- **Ask before fixing.** If you notice a bug, gap, or "problem" that isn't part of
  the task I gave you, STOP and ask whether I want it fixed. Do not assume it needs
  fixing, and do not fix it silently. Point it out in one line, then wait for my call.
- **Do only what's asked.** Don't add error handling, retries, logging, or features
  I didn't request without checking first.
- **Report changes plainly.** After a change, tell me what you changed and why, briefly.
- **Pause when scope balloons.** If a task starts touching many files or feels like
  it's growing beyond what I described, stop and confirm the approach before continuing.