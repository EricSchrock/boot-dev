package main

import (
	"io"
	"net/http"
	"testing"
)

func TestGetHealth(t *testing.T) {
	r, err := http.Get("http://localhost:8080/api/healthz")
	if err != nil {
		t.Fatal(err.Error())
	} else if r.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", r.StatusCode)
	}

	defer r.Body.Close()
	b, err := io.ReadAll(r.Body)
	if err != nil {
		t.Fatal(err.Error())
	} else if string(b) != "OK" {
		t.Errorf("Unexpected body: %v", string(b))
	}
}
