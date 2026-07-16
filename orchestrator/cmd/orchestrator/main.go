package main

import (
	"log"
	"net/http"
	"os"

	analysispipeline "orchestrator/internal/analysis-pipeline"
	"orchestrator/internal/api"
)

func main() {
	// Get env var
	analysisPipelineURL := os.Getenv("PIPELINE_URL")
	if analysisPipelineURL == "" {
		log.Fatal("PIPELINE_URL not set")
	}

	// Get analysis pipeline client
	apc := analysispipeline.New(analysisPipelineURL)

	// Hand down apc client to router
	mux := api.NewRouter(apc)
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
