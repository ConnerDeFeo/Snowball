package analysispipeline

import (
	"net/http"
	"orchestrator/internal/wsproxy"

	"github.com/gorilla/websocket"
)

// HandleDocuments streams document retrieval progress for a ticker.
func (c *Client) HandleDocuments(w http.ResponseWriter, r *http.Request) {
	ticker := r.PathValue("ticker")
	wsproxy.Proxy(w, r, func() (*websocket.Conn, error) {
		return c.DialDocuments(ticker)
	})
}
