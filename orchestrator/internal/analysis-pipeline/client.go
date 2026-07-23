package analysispipeline

// Client structure for main to use
type Client struct {
	baseURL string
}

// Constructor of the struct
func New(baseURL string) *Client {
	return &Client{
		baseURL: baseURL,
	}
}
