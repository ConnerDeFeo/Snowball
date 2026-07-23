package analysispipeline

import (
	"net/http"
)

// HandleGradeSection streams sub-agent progress, then the final graded section.
func (c *Client) HandleGradeSection(w http.ResponseWriter, r *http.Request) {
	c.proxySSE(w, r, "/grade_section")
}
