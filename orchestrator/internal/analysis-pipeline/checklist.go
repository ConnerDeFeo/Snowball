package analysispipeline

import (
	"net/http"

	"orchestrator/internal/proxy"
)

// HandleChecklist forwards checklist CRUD requests (categories, questions)
// to the analysis pipeline. One handler serves every route since
// they all forward the same way: same path, same method, same body.
func (c *Client) HandleChecklist(w http.ResponseWriter, r *http.Request) {
	url := c.baseURL + r.URL.Path
	if r.URL.RawQuery != "" {
		url += "?" + r.URL.RawQuery
	}

	proxy.JSON(w, r, r.Method, url, r.Body)
}
