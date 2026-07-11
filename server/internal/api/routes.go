package api

import (
	"net/http"
	analysispipeline "server/internal/analysis-pipeline"
)

// holds everything the handlers need to reach
type API struct {
	analysisPipeline *analysispipeline.Client
}

func NewRouter(apc *analysispipeline.Client) *http.ServeMux { // capital N — main needs to reach this
	a := &API{analysisPipeline: apc}

	mux := http.NewServeMux()
	// Server routes
	mux.HandleFunc("GET /health", handleHealth)

	// Analysis pipeline routes
	mux.HandleFunc("GET /analysis-pipeline/health", a.handleHealth)
	mux.HandleFunc("POST /documents/{ticker}", a.handleDocuments)
	return mux
}
