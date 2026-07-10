package main

import (
	"log"
	"net/http"
	"os"

	analysispipeline "server/internal/analysis-pipeline"
	"server/internal/api"
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
