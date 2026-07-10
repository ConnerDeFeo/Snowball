package main

import "net/http"

func main() {
	mux := newRouter()
	http.ListenAndServe(":8080", mux)
}
