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

	// Create API struct
	a := &API{analysisPipeline: apc}
	mux := http.NewServeMux()

	// Server routes
	mux.HandleFunc("GET /health", handleHealth)

	// Analysis pipeline routes //
	mux.HandleFunc("GET /analysis-pipeline/health", a.handleHealth)
	// Websocket connections
	mux.HandleFunc("GET /documents/{ticker}", a.handleDocuments)
	return mux
}
