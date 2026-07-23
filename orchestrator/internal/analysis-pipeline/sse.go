package analysispipeline

import (
	"net/http"

	"orchestrator/internal/sse"
)

// proxySSE forwards a GET request (path + query string) to the analysis
// pipeline and streams the response back to the client via the shared sse.Proxy.
func (c *Client) proxySSE(w http.ResponseWriter, r *http.Request, path string) {
	url := c.baseURL + path + "/" + r.PathValue("tckr")

	// If args add them back
	if r.URL.RawQuery != "" {
		url += "?" + r.URL.RawQuery
	}

	sse.Proxy(w, r, http.MethodGet, url, nil)
}
