package sse

import (
	"io"
	"net/http"
)

// Proxy forwards a request to a downstream pipeline and streams the response
// back to the client, flushing after every chunk so SSE frames arrive as
// they're produced instead of buffering.
func Proxy(w http.ResponseWriter, r *http.Request, method, url string, body io.Reader) {
	// Tie the incoming request context from client to outgoing request so the
	// downstream call gets cancelled if the client disconnects.
	req, err := http.NewRequestWithContext(r.Context(), method, url, body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	// Forward the incoming content type when there is a body (e.g. review POSTs JSON).
	if ct := r.Header.Get("Content-Type"); ct != "" {
		req.Header.Set("Content-Type", ct)
	}

	// Send the request
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}
	defer resp.Body.Close() // Clean up when done

	// Check the headers coming back from the downstream container, set them on the response
	for _, h := range []string{"Content-Type", "Cache-Control", "X-Accel-Buffering"} {
		if v := resp.Header.Get(h); v != "" {
			w.Header().Set(h, v)
		}
	}
	w.WriteHeader(resp.StatusCode)

	flusher, _ := w.(http.Flusher) // Check if the writer has a flusher
	buf := make([]byte, 4096)      // Buffer for sending bodies back to client
	for {
		n, rerr := resp.Body.Read(buf) // read into buffer
		if n > 0 {                     // If something actually came
			if _, werr := w.Write(buf[:n]); werr != nil { // write to buffer cancel on err
				return
			}
			if flusher != nil {
				flusher.Flush() // Send message
			}
		}
		if rerr != nil { // Response error or downstream io.EOF mark
			return
		}
	}
}
