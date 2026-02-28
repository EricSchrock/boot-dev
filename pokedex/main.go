package main

import (
	"github.com/EricSchrock/boot-dev/pokedex/internal/pokeapi"
)

func main() {
	cfg := &config{
		nextAreaURL: pokeapi.GetAreasURL(),
		prevAreaURL: "",
	}

	startREPL(cfg)
}
