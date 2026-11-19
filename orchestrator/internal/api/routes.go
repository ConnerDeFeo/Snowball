package api

import (
	"net/http"
	analysispipeline "orchestrator/internal/analysis-pipeline"
	reviewpipeline "orchestrator/internal/review-pipeline"
)

func NewRouter(apc *analysispipeline.Client, rpc *reviewpipeline.Client) *http.ServeMux {

	mux := http.NewServeMux()

	// Server routes
	mux.HandleFunc("GET /health", handleHealth)

	// Analysis pipeline routes
	mux.HandleFunc("GET /analysis-pipeline/health", apc.HandleHealth)
	// SSE streams
	mux.HandleFunc("GET /documents/{tckr}", apc.HandleDocuments)

	// Checklist CRUD (plain JSON, not SSE)
	mux.HandleFunc("GET /checklist", apc.HandleChecklist)
	mux.HandleFunc("POST /checklist", apc.HandleChecklist)
	mux.HandleFunc("GET /checklist/{category_id}", apc.HandleChecklist)
	mux.HandleFunc("PATCH /checklist/{category_id}", apc.HandleChecklist)
	mux.HandleFunc("DELETE /checklist/{category_id}", apc.HandleChecklist)
	mux.HandleFunc("POST /checklist/{category_id}/questions", apc.HandleChecklist)
	mux.HandleFunc("PATCH /checklist/{category_id}/questions/{qid}", apc.HandleChecklist)
	mux.HandleFunc("DELETE /checklist/{category_id}/questions/{qid}", apc.HandleChecklist)

	// Evidence: run (SSE) and read (plain JSON)
	mux.HandleFunc("GET /evidence/run/{tckr}", apc.HandleEvidenceRun)
	mux.HandleFunc("GET /evidence/{tckr}", apc.HandleEvidence)

	// Financial statements (plain JSON)
	mux.HandleFunc("GET /financials/{tckr}", apc.HandleFinancials)

	// Proxy statement (DEF 14A) data (plain JSON)
	mux.HandleFunc("GET /proxies/{tckr}", apc.HandleProxies)

	// 8-K events: list and single markdown body (plain JSON)
	mux.HandleFunc("GET /events/{tckr}", apc.HandleEvents)
	mux.HandleFunc("GET /events/{tckr}/{event_id}", apc.HandleEvents)

	// Insider filings (Form 4, 13D): list and single markdown body (plain JSON)
	mux.HandleFunc("GET /insiders/{tckr}", apc.HandleInsiders)
	mux.HandleFunc("GET /insiders/{tckr}/{filing_id}", apc.HandleInsiders)

	// Company list (plain JSON, not SSE)
	mux.HandleFunc("GET /companies", apc.HandleCompanies)

	// Review pipeline routes
	mux.HandleFunc("GET /review-pipeline/health", rpc.HandleHealth)
	mux.HandleFunc("POST /review/{tckr}", rpc.HandleReview)
	return mux
}
