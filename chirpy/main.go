package main

import (
	"log"
	"net/http"
)

var Port string = "8080"
var Home string = "/app"

func main() {
	log.Println("Starting server...")

	var apiCfg apiConfig
	mux := http.NewServeMux()

	// Front-end website
	mux.Handle(Home+"/*", http.StripPrefix(Home+"/", apiCfg.middlewareMetricsInc(http.FileServer(http.Dir(".")))))

	// Back-end APIs (health)
	mux.HandleFunc("GET "+HealthAPI, healthHandler)

	// Back-end APIs (metrics)
	mux.HandleFunc("GET "+MetricsAPI, apiCfg.metricsHandler)
	mux.HandleFunc(ResetAPI, apiCfg.resetHandler)

	// Back-end APIs (chirps)
	mux.HandleFunc("POST /api/validate_chirp", validateChirpHandler)

	corsMux := middlewareCors(mux)
	server := &http.Server{Addr: ":" + Port, Handler: corsMux}
	err := server.ListenAndServe()
	log.Fatal(err)
}
