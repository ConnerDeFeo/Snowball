package analysispipeline

import (
	"net/http"
)

// proxySSE forwards a GET request (path + query string) to the analysis
// pipeline and streams the response back to the client, flushing after
// every chunk so SSE frames arrive as they're produced instead of buffering.
func (c *Client) proxySSE(w http.ResponseWriter, r *http.Request, path string) {
	url := c.baseURL + path + "/" + r.PathValue("tckr")

	// If args add them back
	if r.URL.RawQuery != "" {
		url += "?" + r.URL.RawQuery
	}

	// Create the outgoing reqeust to python container
	// Tie the incoming reqeust context from client to outgoing request to the python api is the r.Context()
	// Then the method is get, url is the one above, and no body means nil
	req, err := http.NewRequestWithContext(r.Context(), http.MethodGet, url, nil)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Send the request
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}
	defer resp.Body.Close() // Clean up when dones

	// Check the headers coming back from python container, set them to return reqeust
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
			if _, werr := w.Write(buf[:n]); werr != nil { // write to buffer cancle on err
				return
			}
			if flusher != nil {
				flusher.Flush() // Send message
			}
		}
		if rerr != nil { // Response error or python io.EOF mark
			return
		}
	}
}
