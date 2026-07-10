package analysispipeline

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

// Client structure for main to use
type Client struct {
	baseURL string
}

// Constructor of the struct
func New(baseURL string) *Client {
	return &Client{baseURL: baseURL}
}

// Struct for storing the request
type docRequest struct {
	FromDate string `json:"from_date"`
	ToDate   string `json:"to_date"`
}

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
		return fmt.Errorf("pipeline rejected request: from_date and to_date required")
	default:
		return fmt.Errorf("pipeline returned unexpected status: %d", resp.StatusCode)
	}
}
