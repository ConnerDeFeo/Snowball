package analysispipeline

import (
	"net/http"
	"orchestrator/internal/wsproxy"

	"github.com/gorilla/websocket"
)

// HandleGradeSection streams sub-agent progress, then the final graded section.
func (c *Client) HandleGradeSection(w http.ResponseWriter, r *http.Request) {
	tckr := r.PathValue("tckr")
	wsproxy.Proxy(w, r, func() (*websocket.Conn, error) {
		return c.DialGradeSection(tckr)
	})
}
