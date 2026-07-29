package analysispipeline

import (
	"net/http"

	"orchestrator/internal/proxy"
)

// HandleGrades forwards read-only grade/company-list requests to the
// analysis pipeline. Same shape as HandleRubric: same path, same method
// (always GET here), query string passed through untouched.
func (c *Client) HandleGrades(w http.ResponseWriter, r *http.Request) {
	url := c.baseURL + r.URL.Path
	if r.URL.RawQuery != "" {
		url += "?" + r.URL.RawQuery
	}

	proxy.JSON(w, r, r.Method, url, r.Body)
}
