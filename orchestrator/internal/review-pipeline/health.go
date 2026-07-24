package reviewpipeline

import (
	"net/http"

	"orchestrator/internal/proxy"
)

// HandleHealth reports whether the review pipeline is reachable and healthy.
func (c *Client) HandleHealth(w http.ResponseWriter, r *http.Request) {
	proxy.JSON(w, r, http.MethodGet, c.baseURL+"/health", nil)
}
