package analysispipeline

import (
	"net/http"
)

// HandleGradeSection streams sub-agent progress, then the final graded section.
func (c *Client) HandleGradeSection(w http.ResponseWriter, r *http.Request) {
	c.proxySSE(w, r, "/grade_section")
}

// HandleGradeAll streams sub-agent progress, then the final graded company (all categories).
func (c *Client) HandleGradeAll(w http.ResponseWriter, r *http.Request) {
	c.proxySSE(w, r, "/grade_all")
}
