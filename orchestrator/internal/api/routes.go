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
	// Websocket connections
	mux.HandleFunc("GET /documents/{tckr}", apc.HandleDocuments)
	mux.HandleFunc("GET /grade_section/{tckr}", apc.HandleGradeSection)

	// Review pipeline routes
	mux.HandleFunc("GET /review-pipeline/health", rpc.HandleHealth)
	mux.HandleFunc("POST /review/{tckr}", rpc.HandleReview)
	return mux
}
