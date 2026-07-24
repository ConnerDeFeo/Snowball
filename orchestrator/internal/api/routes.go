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
	mux.HandleFunc("GET /grade_section/{tckr}", apc.HandleGradeSection)
	mux.HandleFunc("GET /grade_all/{tckr}", apc.HandleGradeAll)

	// Rubric CRUD (plain JSON, not SSE)
	mux.HandleFunc("POST /rubric/{rubric_category}", apc.HandleRubric)
	mux.HandleFunc("PATCH /rubric/{rubric_category}", apc.HandleRubric)
	mux.HandleFunc("DELETE /rubric/{rubric_category}", apc.HandleRubric)
	mux.HandleFunc("POST /rubric/{rubric_category}/sub_agent", apc.HandleRubric)
	mux.HandleFunc("PATCH /rubric/{rubric_category}/sub_agent", apc.HandleRubric)
	mux.HandleFunc("DELETE /rubric/{rubric_category}/sub_agent", apc.HandleRubric)

	// Review pipeline routes
	mux.HandleFunc("GET /review-pipeline/health", rpc.HandleHealth)
	mux.HandleFunc("POST /review/{tckr}", rpc.HandleReview)
	return mux
}
