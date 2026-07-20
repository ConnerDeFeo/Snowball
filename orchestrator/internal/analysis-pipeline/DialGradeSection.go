package analysispipeline

import "github.com/gorilla/websocket"

// DialGradeSection opens a websocket to the analysis-pipeline's section
// grading endpoint for `ticker`. Caller owns the returned connection.
func (c *Client) DialGradeSection(ticker string) (*websocket.Conn, error) {
	return c.dialPipeline("/grade_section", ticker)
}
