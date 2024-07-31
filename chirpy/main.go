package main

import (
	"log"
	"net/http"
)

var Port string = "8080"

func main() {
	log.Println("Starting server...")

	var apiCfg apiConfig
	mux := http.NewServeMux()

	// Front-end website
	mux.Handle("/app/*", http.StripPrefix("/app/", apiCfg.middlewareMetricsInc(http.FileServer(http.Dir(".")))))

	// Back-end APIs (health)
	mux.HandleFunc("GET "+HealthAPI, healthHandler)

	// Back-end APIs (metrics)
	mux.HandleFunc("GET /admin/metrics", apiCfg.metricsHandler)
	mux.HandleFunc("/api/reset", apiCfg.resetHandler)

	// Back-end APIs (chirps)
	mux.HandleFunc("POST /api/validate_chirp", validateChirpHandler)

	corsMux := middlewareCors(mux)
	server := &http.Server{Addr: ":" + Port, Handler: corsMux}
	err := server.ListenAndServe()
	log.Fatal(err)
}
