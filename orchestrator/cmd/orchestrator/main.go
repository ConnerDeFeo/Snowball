package main

import (
	"log"
	"net/http"
	"os"

	analysispipeline "orchestrator/internal/analysis-pipeline"
	"orchestrator/internal/api"
	reviewpipeline "orchestrator/internal/review-pipeline"
)

func main() {
	// Get env var
	analysisPipelineURL := os.Getenv("ANALYSIS_PIPELINE_URL")
	if analysisPipelineURL == "" {
		log.Fatal("ANALYSIS_PIPELINE_URL not set")
	}
	reviewPipelineURL := os.Getenv("REVIEW_PIPELINE_URL")
	if reviewPipelineURL == "" {
		log.Fatal("REVIEW_PIPELINE_URL not set")
	}

	// Get analysis pipeline client
	apc := analysispipeline.New(analysisPipelineURL)
	// Get review pipeline client
	rpc := reviewpipeline.New(reviewPipelineURL)

	// Hand down clients to router
	mux := api.NewRouter(apc, rpc)
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
