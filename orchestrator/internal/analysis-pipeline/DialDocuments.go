package analysispipeline

import "github.com/gorilla/websocket"

// DialDocuments opens a websocket to the analysis-pipeline's document
// retrieval endpoint for `ticker`. Caller owns the returned connection.
func (c *Client) DialDocuments(ticker string) (*websocket.Conn, error) {
	return c.dialPipeline("/documents", ticker)
}
