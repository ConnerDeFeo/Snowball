package api

import (
	"fmt"
	"net/http"

	"github.com/gorilla/websocket"
)

func (a *API) handleHealth(w http.ResponseWriter, r *http.Request) {
	if err := a.analysisPipeline.Health(); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
	fmt.Fprintln(w, "ok")
}

// Streams
func (a *API) handleDocuments(w http.ResponseWriter, r *http.Request) {
	ticker := r.PathValue("ticker")
	a.proxyWebSocket(w, r, func() (*websocket.Conn, error) {
		return a.analysisPipeline.DialDocuments(ticker)
	})
}
