package api

import (
	"net/http"

	"github.com/gorilla/websocket"
)

// Streams sub-agent progress, then the final graded section.
func (a *API) handleGradeSection(w http.ResponseWriter, r *http.Request) {
	tckr := r.PathValue("tckr")
	a.proxyWebSocket(w, r, func() (*websocket.Conn, error) {
		return a.analysisPipeline.DialGradeSection(tckr)
	})
}
