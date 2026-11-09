package analysispipeline

import (
	"net/http"

	"orchestrator/internal/proxy"
)

// HandleEvidenceRun streams checklist run progress, then the final evidence.
func (c *Client) HandleEvidenceRun(w http.ResponseWriter, r *http.Request) {
	c.proxySSE(w, r, "/evidence/run")
}

// HandleEvidence forwards a read of stored evidence (plain JSON, not SSE);
// query string (years, category_id, question_id) passed through untouched.
func (c *Client) HandleEvidence(w http.ResponseWriter, r *http.Request) {
	url := c.baseURL + r.URL.Path
	if r.URL.RawQuery != "" {
		url += "?" + r.URL.RawQuery
	}

	proxy.JSON(w, r, r.Method, url, r.Body)
}
