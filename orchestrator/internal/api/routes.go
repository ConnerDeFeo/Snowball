package api

import (
	"net/http"
	analysispipeline "orchestrator/internal/analysis-pipeline"
)

// holds everything the handlers need to reach
type API struct {
	analysisPipeline *analysispipeline.Client
}

func NewRouter(apc *analysispipeline.Client) *http.ServeMux {

	a := &API{analysisPipeline: apc}
	mux := http.NewServeMux()

	// Server routes
	mux.HandleFunc("GET /health", handleHealth)
	mux.HandleFunc("GET /ws", handleWebSocket)

	// Analysis pipeline routes
	mux.HandleFunc("GET /analysis-pipeline/health", a.handleHealth)
	mux.HandleFunc("POST /documents/{ticker}", a.handleDocuments)
	return mux
}
