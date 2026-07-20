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

var upgrader = websocket.Upgrader{
	// Allow any origin
	CheckOrigin: func(r *http.Request) bool { return true },
}

// Streams
func (a *API) handleDocuments(w http.ResponseWriter, r *http.Request) {
	ticker := r.PathValue("ticker")

	// Upgrade connection to ws
	client, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		return
	}
	defer client.Close() // Close connection when done

	// Get the connection stream
	conn, err := a.analysisPipeline.DialDocuments(ticker)
	if err != nil {
		// Close message on err
		client.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseInternalServerErr, err.Error()))
		return
	}
	defer conn.Close() // Close connection when done

	// Pipe for two goroutintes to talk to each other
	done := make(chan struct{}, 2)
	// Send mesage from one ws to the other
	pump := func(dst, src *websocket.Conn) {
		// On function end, send empty struct to pipe
		defer func() { done <- struct{}{} }()
		for {
			// Read message from src connection
			msgType, msg, err := src.ReadMessage()
			if err != nil {
				return
			}
			// Write to dst connection
			if err := dst.WriteMessage(msgType, msg); err != nil {
				return
			}
		}
	}

	go pump(conn, client) // browser -> pipeline | goroutine
	go pump(client, conn) // pipeline -> browser | goroutine

	<-done // Wait for signal from either connection
}
