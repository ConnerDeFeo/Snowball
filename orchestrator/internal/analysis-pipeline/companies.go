package analysispipeline

import (
	"net/http"

	"orchestrator/internal/proxy"
)

// HandleCompanies forwards the company list request to the analysis pipeline.
func (c *Client) HandleCompanies(w http.ResponseWriter, r *http.Request) {
	proxy.JSON(w, r, r.Method, c.baseURL+r.URL.Path, r.Body)
}
