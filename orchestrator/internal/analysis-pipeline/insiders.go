package analysispipeline

import (
	"net/http"

	"orchestrator/internal/proxy"
)

// HandleInsiders forwards reads of cached Form 4 and 13D filings (plain
// JSON, not SSE): the list (with years in the query string) and a single filing's markdown.
func (c *Client) HandleInsiders(w http.ResponseWriter, r *http.Request) {
	url := c.baseURL + r.URL.Path
	if r.URL.RawQuery != "" {
		url += "?" + r.URL.RawQuery
	}

	proxy.JSON(w, r, r.Method, url, r.Body)
}
