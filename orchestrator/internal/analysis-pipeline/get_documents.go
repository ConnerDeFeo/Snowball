package analysispipeline

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

// Function for client to get Documents
func (c *Client) GetDocuments(ticker, fromDate, toDate string) error {
	reqBody := docRequest{
		FromDate: fromDate,
		ToDate:   toDate,
	}

	//convert data to bytes
	data, err := json.Marshal(reqBody)

	// Error occured, stop
	if err != nil {
		return fmt.Errorf("encoding request body: %w", err)
	}

	// base url for the current client class including the tckr passed down
	url := c.baseURL + "/documents/" + ticker

	resp, err := http.Post(url, "application/json", bytes.NewReader(data))
	if err != nil {
		return fmt.Errorf("calling pipeline: %w", err)
	}
	// Close response stream
	defer resp.Body.Close()

	// Check status code
	switch resp.StatusCode {
	case http.StatusOK:
		return nil
	case http.StatusNotFound:
		return fmt.Errorf("no company found for ticker: %s", ticker)
	case http.StatusBadRequest:
		return fmt.Errorf("pipeline rejected request: from_date and to_date required and must be 6 year gap maximum")
	default:
		return fmt.Errorf("pipeline returned unexpected status: %d", resp.StatusCode)
	}
}
