package api

import (
	"net/http"
	analysispipeline "orchestrator/internal/analysis-pipeline"
)

func NewRouter(apc *analysispipeline.Client) *http.ServeMux {

	mux := http.NewServeMux()

	// Server routes
	mux.HandleFunc("GET /health", handleHealth)

	// Analysis pipeline routes //
	mux.HandleFunc("GET /analysis-pipeline/health", apc.HandleHealth)
	// Websocket connections
	mux.HandleFunc("GET /documents/{ticker}", apc.HandleDocuments)
	mux.HandleFunc("GET /grade_section/{tckr}", apc.HandleGradeSection)
	return mux
}
