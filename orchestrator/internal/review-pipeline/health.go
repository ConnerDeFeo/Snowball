package reviewpipeline

import (
	"fmt"
	"net/http"
)

func (c *Client) Health() error {
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
