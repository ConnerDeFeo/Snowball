package analysispipeline

import (
	"net/http"

	"orchestrator/internal/proxy"
)

// HandleEvents forwards reads of cached 8-Ks (plain JSON, not SSE): the list
// (with years in the query string) and a single event's markdown.
func (c *Client) HandleEvents(w http.ResponseWriter, r *http.Request) {
	url := c.baseURL + r.URL.Path
	if r.URL.RawQuery != "" {
		url += "?" + r.URL.RawQuery
	}

	proxy.JSON(w, r, r.Method, url, r.Body)
}
