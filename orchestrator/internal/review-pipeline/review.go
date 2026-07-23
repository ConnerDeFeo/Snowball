package reviewpipeline

import (
	"net/http"

	"orchestrator/internal/sse"
)

// HandleReview forwards a review request for a ticker to the review pipeline
// and streams its SSE response back to the caller.
func (c *Client) HandleReview(w http.ResponseWriter, r *http.Request) {
	url := c.baseURL + "/review/" + r.PathValue("tckr")
	sse.Proxy(w, r, http.MethodPost, url, r.Body)
}
