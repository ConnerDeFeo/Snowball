package main

import (
	"net/http"
	"server/internal/api"
)

func main() {
	mux := api.NewRouter()
	http.ListenAndServe(":8080", mux)
}
