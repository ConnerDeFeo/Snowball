package api

import (
	"encoding/json"
	"net/http"
)

// Struct for storing the request
type documentRequest struct {
	FromDate string `json:"from_date"`
	ToDate   string `json:"to_date"`
}

func (a *API) handleDocuments(w http.ResponseWriter, r *http.Request) {

	var req documentRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON body", http.StatusBadRequest)
		return
	}

	ticker := r.PathValue("ticker")
	if err := a.analysisPipeline.GetDocuments(ticker, req.FromDate, req.ToDate); err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}

	w.WriteHeader(http.StatusOK)
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
}
