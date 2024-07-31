package main

import (
	"io"
	"net/http"
	"testing"
)

var Host string = "http://localhost"

func TestGetHealth(t *testing.T) {
	r, err := http.Get(Host + ":" + Port + HealthAPI)
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
