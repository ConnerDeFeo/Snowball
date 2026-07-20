package api

import (
	"net/http"

	"github.com/gorilla/websocket"
)

// Streams sub-agent progress, then the final graded section.
func (a *API) handleGradeSection(w http.ResponseWriter, r *http.Request) {
	tckr := r.PathValue("tckr")

	// Upgrade connection to ws
	client, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		return
	}
	defer client.Close() // Close connection when done

	// Get the connection stream
	conn, err := a.analysisPipeline.DialGradeSection(tckr)
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
