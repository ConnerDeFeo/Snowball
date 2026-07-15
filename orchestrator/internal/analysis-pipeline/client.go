package analysispipeline

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
