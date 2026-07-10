package api

import (
	"fmt"
	"net/http"
)

func handleHealth(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "ok")
}
