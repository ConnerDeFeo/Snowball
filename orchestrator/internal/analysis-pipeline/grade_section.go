package analysispipeline

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

// Mirrors the python service's GradeSectionRequest body.
type GradeSectionRequest struct {
	StartDate      string `json:"start_date"`
	EndDate        string `json:"end_date"`
	RubricCategory string `json:"rubric_category"`
}

// GradeSection posts to the analysis-pipeline's /grade_section/{tckr} and
// returns the raw JSON response body for the caller to forward as-is.
func (c *Client) GradeSection(tckr string, req GradeSectionRequest) ([]byte, error) {
	body, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("marshaling request: %w", err)
	}

	url := c.baseURL + "/grade_section/" + tckr
	resp, err := http.Post(url, "application/json", bytes.NewReader(body))
	if err != nil {
		return nil, fmt.Errorf("calling pipeline: %w", err)
	}
	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("reading pipeline response: %w", err)
	}

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("pipeline returned unexpected status %d: %s", resp.StatusCode, respBody)
	}

	return respBody, nil
}
