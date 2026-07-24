package analysispipeline

import (
	"net/http"

	"orchestrator/internal/proxy"
)

// HandleRubric forwards rubric CRUD requests to the analysis pipeline. One
// handler serves all six routes (rubric + sub_agent, POST/PATCH/DELETE) since
// they all forward the same way: same path, same method, same body.
func (c *Client) HandleRubric(w http.ResponseWriter, r *http.Request) {
	url := c.baseURL + r.URL.Path

	// DELETE /rubric/{category}/sub_agent passes form + section as query params.
	if r.URL.RawQuery != "" {
		url += "?" + r.URL.RawQuery
	}

	proxy.JSON(w, r, r.Method, url, r.Body)
}
