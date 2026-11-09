package analysispipeline

import (
	"net/http"

	"orchestrator/internal/proxy"
)

// HandleFinancials forwards a read of cached financial statements (plain JSON,
// not SSE); query string (years) passed through untouched.
func (c *Client) HandleFinancials(w http.ResponseWriter, r *http.Request) {
	url := c.baseURL + r.URL.Path
	if r.URL.RawQuery != "" {
		url += "?" + r.URL.RawQuery
	}

	proxy.JSON(w, r, r.Method, url, r.Body)
}
