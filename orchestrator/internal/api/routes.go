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

	// Company list (plain JSON, not SSE)
	mux.HandleFunc("GET /companies", apc.HandleCompanies)

	// Review pipeline routes
	mux.HandleFunc("GET /review-pipeline/health", rpc.HandleHealth)
	mux.HandleFunc("POST /review/{tckr}", rpc.HandleReview)
	return mux
}
