package main

import (
	"bytes"
	"io"
	"net/http"
	"strings"
	"testing"
)

var host string = "http://localhost"

func postRequestTest(t *testing.T, api string, requestBody string, responseStatus int, responseBody string) {
	req, err := http.NewRequest(http.MethodPost, host+":"+port+api, bytes.NewReader([]byte(requestBody)))
	if err != nil {
		t.Fatal(err.Error())
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatal(err.Error())
	} else if resp.StatusCode != responseStatus {
		t.Errorf("Unexpected status: %v", resp.StatusCode)
	}

	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err.Error())
	} else if string(body) != responseBody {
		t.Errorf("Unexpected body: %v", string(body))
	}
}

func TestWelcome(t *testing.T) {
	resp, err := http.Get(host + ":" + port + home)
	if err != nil {
		t.Fatal(err.Error())
	} else if resp.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", resp.StatusCode)
	}

	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err.Error())
	} else if !strings.Contains(string(body), "Welcome to Chirpy") {
		t.Errorf("Unexpected body: %v", string(body))
	}
}

func TestLogo(t *testing.T) {
	resp, err := http.Get(host + ":" + port + assets)
	if err != nil {
		t.Fatal(err.Error())
	} else if resp.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", resp.StatusCode)
	}

	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err.Error())
	} else if !strings.Contains(string(body), `<a href="logo.png">logo.png</a>`) {
		t.Errorf("Unexpected body: %v", string(body))
	}
}

func TestHealth(t *testing.T) {
	resp, err := http.Get(host + ":" + port + healthAPI)
	if err != nil {
		t.Fatal(err.Error())
	} else if resp.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", resp.StatusCode)
	}

	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err.Error())
	} else if string(body) != "OK" {
		t.Errorf("Unexpected body: %v", string(body))
	}
}

func TestMetrics(t *testing.T) {
	resp, err := http.Get(host + ":" + port + resetAPI)
	if err != nil {
		t.Fatal(err.Error())
	} else if resp.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", resp.StatusCode)
	}

	resp, err = http.Get(host + ":" + port + metricsAPI)
	if err != nil {
		t.Fatal(err.Error())
	} else if resp.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", resp.StatusCode)
	}

	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err.Error())
	} else if !strings.Contains(string(body), "0 times") {
		t.Errorf("Unexpected body: %v", string(body))
	}

	resp, err = http.Get(host + ":" + port + home)
	if err != nil {
		t.Fatal(err.Error())
	} else if resp.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", resp.StatusCode)
	}

	resp, err = http.Get(host + ":" + port + metricsAPI)
	if err != nil {
		t.Fatal(err.Error())
	} else if resp.StatusCode != http.StatusOK {
		t.Errorf("Unexpected status: %v", resp.StatusCode)
	}

	defer resp.Body.Close()
	body, err = io.ReadAll(resp.Body)
	if err != nil {
		t.Fatal(err.Error())
	} else if !strings.Contains(string(body), "1 times") {
		t.Errorf("Unexpected body: %v", string(body))
	}
}

func TestChirp(t *testing.T) {
	postRequestTest(t, chirpAPI, `{"body": "hello"}`, http.StatusOK, `{"cleaned_body":"hello"}`)
}

func TestChirpLengthLimit(t *testing.T) {
	postRequestTest(t, chirpAPI, `{"body": "`+strings.Repeat("hello", (chirpLengthLimit/len("hello"))+1)+`"}`, http.StatusBadRequest, `{"error":"Chirp is too long"}`)
}

func TestChirpProfanityFilter(t *testing.T) {
	for _, profanity := range profanities {
		t.Run(profanity, func(t *testing.T) {
			postRequestTest(t, chirpAPI, `{"body": "abc `+profanity+` 123"}`, http.StatusOK, `{"cleaned_body":"abc **** 123"}`)
		})
	}
}
