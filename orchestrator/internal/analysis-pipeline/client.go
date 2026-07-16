package analysispipeline

import "strings"

// Client structure for main to use
type Client struct {
	baseURL string
	wsURL   string
}

// Constructor of the struct
func New(baseURL string) *Client {
	return &Client{
		baseURL: baseURL,
		wsURL:   toWebsocketScheme(baseURL),
	}
}

// http(s):// -> ws(s):// so the same configured base URL can be dialed as a websocket
func toWebsocketScheme(url string) string {
	switch {
	case strings.HasPrefix(url, "https://"):
		return "wss://" + strings.TrimPrefix(url, "https://")
	case strings.HasPrefix(url, "http://"):
		return "ws://" + strings.TrimPrefix(url, "http://")
	default:
		return url
	}
}
