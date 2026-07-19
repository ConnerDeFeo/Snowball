package api

import (
	"encoding/json"
	"net/http"

	analysispipeline "orchestrator/internal/analysis-pipeline"
)

func (a *API) handleGradeSection(w http.ResponseWriter, r *http.Request) {
	tckr := r.PathValue("tckr")

	var req analysispipeline.GradeSectionRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	respBody, err := a.analysisPipeline.GradeSection(tckr, req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(respBody)
}
