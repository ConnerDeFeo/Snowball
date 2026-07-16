package api

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{}

// Echoes back whatever the client sends, so you can see the connection working.
func handleWebSocket(w http.ResponseWriter, r *http.Request) {
	// Upgrade connection to websocket and gets connection stream
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("websocket upgrade failed:", err)
		return
	}
	defer conn.Close()

	// Loop until error
	for {
		// Fetch message type, message, and error from connection stream, blocking call
		msgType, msg, err := conn.ReadMessage()
		if err != nil {
			break
		}
		// write back message to connection, if error stop
		if err := conn.WriteMessage(msgType, msg); err != nil {
			break
		}
	}
}
