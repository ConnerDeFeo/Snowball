package analysispipeline

import (
	"fmt"

	"github.com/gorilla/websocket"
)

// DialDocuments opens a websocket to the analysis-pipeline's document
// retrieval endpoint for `ticker`. Caller owns the returned connection.
func (c *Client) DialDocuments(ticker string) (*websocket.Conn, error) {
	url := c.wsURL + "/documents/" + ticker

	// Opens ws wioth connection stream
	conn, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		return nil, fmt.Errorf("dialing pipeline: %w", err)
	}
	return conn, nil
}
