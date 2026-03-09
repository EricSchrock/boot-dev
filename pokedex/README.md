# Pokedex

Pokedex created using [PokéAPI v2](https://pokeapi.co/docs/v2).

## Run

```sh
$ go run .
Pokedex > help
Welcome to the Pokedex!
Usage:

pokedex: List the Pokemon in your Pokedex
exit: Exit the Pokedex
help: Displays a help message
map : Displays the next 20 map locations
mapb: Displays the last 20 map locations
explore: Lists the Pokemon found at the provided location
catch: Attempt to catch a Pokemon
inspect: Inspect a Pokemon from your Pokedex
Pokedex >
```

## Dev

```sh
$ go build ./...
$ go fmt ./...
$ go test ./...
```
