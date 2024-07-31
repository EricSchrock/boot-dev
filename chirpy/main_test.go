package main

import (
	"io"
	"net/http"
	"strings"
	"testing"
)

var Host string = "http://localhost"

func TestWelcome(t *testing.T) {
	r, err := http.Get(Host + ":" + Port + Home)
	if err != nil {
		t.Fatal(err.Error())
	} else if r.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", r.StatusCode)
	}

	defer r.Body.Close()
	b, err := io.ReadAll(r.Body)
	if err != nil {
		t.Fatal(err.Error())
	} else if !strings.Contains(string(b), "Welcome to Chirpy") {
		t.Errorf("Unexpected body: %v", string(b))
	}
}

func TestLogo(t *testing.T) {
	r, err := http.Get(Host + ":" + Port + Assets)
	if err != nil {
		t.Fatal(err.Error())
	} else if r.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", r.StatusCode)
	}

	defer r.Body.Close()
	b, err := io.ReadAll(r.Body)
	if err != nil {
		t.Fatal(err.Error())
	} else if !strings.Contains(string(b), `<a href="logo.png">logo.png</a>`) {
		t.Errorf("Unexpected body: %v", string(b))
	}
}

func TestHealth(t *testing.T) {
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

func TestMetrics(t *testing.T) {
	r, err := http.Get(Host + ":" + Port + ResetAPI)
	if err != nil {
		t.Fatal(err.Error())
	} else if r.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", r.StatusCode)
	}

	r, err = http.Get(Host + ":" + Port + MetricsAPI)
	if err != nil {
		t.Fatal(err.Error())
	} else if r.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", r.StatusCode)
	}

	defer r.Body.Close()
	b, err := io.ReadAll(r.Body)
	if err != nil {
		t.Fatal(err.Error())
	} else if !strings.Contains(string(b), "0 times") {
		t.Errorf("Unexpected body: %v", string(b))
	}

	r, err = http.Get(Host + ":" + Port + Home)
	if err != nil {
		t.Fatal(err.Error())
	} else if r.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", r.StatusCode)
	}

	r, err = http.Get(Host + ":" + Port + MetricsAPI)
	if err != nil {
		t.Fatal(err.Error())
	} else if r.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", r.StatusCode)
	}

	defer r.Body.Close()
	b, err = io.ReadAll(r.Body)
	if err != nil {
		t.Fatal(err.Error())
	} else if !strings.Contains(string(b), "1 times") {
		t.Errorf("Unexpected body: %v", string(b))
	}
}
