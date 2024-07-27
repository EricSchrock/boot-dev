package main

import (
	"encoding/json"
	"log"
	"net/http"
	"strings"
)

func validateChirpHandler(w http.ResponseWriter, r *http.Request) {
	type request struct {
		Body string `json:"body"`
	}

	decoder := json.NewDecoder(r.Body)
	req := request{}
	err := decoder.Decode(&req)
	if err != nil {
		log.Print(err)
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	if len(req.Body) > 140 {
		respondWithError(w, http.StatusBadRequest, "Chirp is too long")
		return
	}

	type response struct {
		Body string `json:"cleaned_body"`
	}

	respondWithJSON(w, http.StatusOK, response{cleanChirp(req.Body)})
}

func cleanChirp(chirp string) string {
	words := strings.Split(chirp, " ")
	for i, word := range words {
		for _, profanity := range []string{"kerfuffle", "sharbert", "fornax"} {
			if strings.ToLower(word) == profanity {
				words[i] = "****"
				break
			}
		}
	}

	return strings.Join(words, " ")
}

func respondWithError(w http.ResponseWriter, status int, message string) {
	type response struct {
		Error string `json:"error"`
	}

	resp := response{message}
	data, err := json.Marshal(resp)
	if err != nil {
		log.Print(err)
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	w.Write(data)
}

func respondWithJSON(w http.ResponseWriter, status int, payload interface{}) {
	data, err := json.Marshal(payload)
	if err != nil {
		log.Print(err)
		w.WriteHeader(http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	w.Write(data)
}
