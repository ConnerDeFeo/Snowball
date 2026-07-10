package api

import "net/http"

func NewRouter() *http.ServeMux { // capital N — main needs to reach this
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", handleHealth)
	return mux
}
