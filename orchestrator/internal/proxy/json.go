package proxy

import (
	"io"
	"net/http"
	"time"
)

// Unlike the SSE path, these are short request/response round trips, so a
// hung downstream shouldn't be able to pin a connection open forever.
var client = &http.Client{Timeout: 30 * time.Second}

// JSON forwards a request to a downstream pipeline and copies its response
// back to the client in one shot, preserving the upstream status code.
func JSON(w http.ResponseWriter, r *http.Request, method, url string, body io.Reader) {
	// Tie the incoming request context from client to outgoing request so the
	// downstream call gets cancelled if the client disconnects.
	req, err := http.NewRequestWithContext(r.Context(), method, url, body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	// Forward the incoming content type when there is a body.
	if ct := r.Header.Get("Content-Type"); ct != "" {
		req.Header.Set("Content-Type", ct)
	}

	// Send the request
	resp, err := client.Do(req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}
	defer resp.Body.Close() // Clean up when done

	if ct := resp.Header.Get("Content-Type"); ct != "" {
		w.Header().Set("Content-Type", ct)
	}
	// Forward the upstream status verbatim so 400/404/409/422 all reach the caller.
	w.WriteHeader(resp.StatusCode)

	io.Copy(w, resp.Body)
}
