package reviewpipeline

import (
	"fmt"
	"net/http"
)

func (c *Client) health() error {
	url := c.baseURL + "/health"
	resp, err := http.Get(url)

	if err != nil {
		return fmt.Errorf("calling pipeline: %w", err)
	}
	// Close response stream
	defer resp.Body.Close()

	// Check status code
	if resp.StatusCode == http.StatusOK {
		return nil
	}
	return fmt.Errorf("pipeline returned unexpected status: %d", resp.StatusCode)
}

// HandleHealth reports whether the analysis pipeline is reachable and healthy.
func (c *Client) HandleHealth(w http.ResponseWriter, r *http.Request) {
	if err := c.health(); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusOK)
	fmt.Fprintln(w, "ok")
}
