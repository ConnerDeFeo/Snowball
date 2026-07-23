package analysispipeline

import (
	"net/http"
)

// HandleDocuments streams document retrieval progress for a ticker.
func (c *Client) HandleDocuments(w http.ResponseWriter, r *http.Request) {
	c.proxySSE(w, r, "/documents")
}
