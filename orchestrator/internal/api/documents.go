package api

import (
	"encoding/json"
	"fmt"
	"net/http"
)

// Struct for storing the request
type documentRequest struct {
	FromDate string `json:"from_date"`
	ToDate   string `json:"to_date"`
}

func (a *API) handleDocuments(w http.ResponseWriter, r *http.Request) {

	var req documentRequest
	// Decode body to json stream, write contents to request structure
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON body", http.StatusBadRequest)
		return
	}

	// Get ticker from the url
	ticker := r.PathValue("ticker")
	// Fetch documetns from analysis-pipeline
	if err := a.analysisPipeline.GetDocuments(ticker, req.FromDate, req.ToDate); err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}

	w.WriteHeader(http.StatusOK)
	// Send back map encoded map --> json with resp
	json.NewEncoder(w).Encode(map[string]string{
		"status": "ok",
		"ticker": ticker,
	})
}

func (a *API) handleHealth(w http.ResponseWriter, r *http.Request) {
	if err := a.analysisPipeline.Health(); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
	fmt.Fprintln(w, "ok")
}
