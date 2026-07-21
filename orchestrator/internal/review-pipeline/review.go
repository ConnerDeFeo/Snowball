package reviewpipeline

import (
	"io"
	"net/http"
)

// HandleReview forwards a review request for a ticker to the review pipeline
// and returns its JSON response to the caller.
func (c *Client) HandleReview(w http.ResponseWriter, r *http.Request) {
	tckr := r.PathValue("tckr")
	resp, err := http.Post(c.baseURL+"/review/"+tckr, "application/json", r.Body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	w.Header().Set("Content-Type", resp.Header.Get("Content-Type"))
	w.WriteHeader(resp.StatusCode)
	io.Copy(w, resp.Body)
}
