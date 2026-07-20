package analysispipeline

import (
	"fmt"
	"github.com/gorilla/websocket"
)

// dialPipeline opens a websocket to the analysis-pipeline at `path` for `ticker`.
// Caller owns the returned connection.
func (c *Client) dialPipeline(path, ticker string) (*websocket.Conn, error) {
	url := c.wsURL + path + "/" + ticker
	conn, _, err := websocket.DefaultDialer.Dial(url, nil)
	if err != nil {
		return nil, fmt.Errorf("dialing pipeline: %w", err)
	}
	return conn, nil
}
