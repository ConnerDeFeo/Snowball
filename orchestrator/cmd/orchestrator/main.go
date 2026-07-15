package main

import (
	"log"
	"net/http"
	"os"

	analysispipeline "orchestrator/internal/analysis-pipeline"
	"orchestrator/internal/api"
)

func main() {
	analysisPipelineURL := os.Getenv("PIPELINE_URL")
	if analysisPipelineURL == "" {
		log.Fatal("PIPELINE_URL not set")
	}

	apc := analysispipeline.New(analysisPipelineURL)

	mux := api.NewRouter(apc)
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
