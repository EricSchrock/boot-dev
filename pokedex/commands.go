package main

import (
	"fmt"
	"os"

	"github.com/EricSchrock/boot-dev/pokedex/internal/pokeapi"
)

type cliCommand struct {
	description string
	callback    func() error
}

var commands = map[string]cliCommand{}

func registerCommands() {
	commands["exit"] = cliCommand{
		description: "Exit the Pokedex",
		callback:    commandExit,
	}

	commands["help"] = cliCommand{
		description: "Displays a help message",
		callback:    commandHelp,
	}

	commands["map"] = cliCommand{
		description: "Displays the next 20 map locations",
		callback:    commandMap,
	}

	commands["mapb"] = cliCommand{
		description: "Displays the last 20 map locations",
		callback:    commandMapBack,
	}
}

func commandExit() error {
	fmt.Println("Closing the Pokedex... Goodbye!")
	os.Exit(0)
	return nil
}

func commandHelp() error {
	fmt.Println("Welcome to the Pokedex!")
	fmt.Println("Usage:")
	fmt.Println()
	for k, v := range commands {
		fmt.Printf("%-4s: %s\n", k, v.description)
	}
	return nil
}

var next_map string = "https://pokeapi.co/api/v2/location-area?offset=0&limit=20"
var prev_map string = ""

func commandMap() error {
	if next_map == "" {
		fmt.Println("You're on the last page")
		return nil
	}

	var err error
	next_map, prev_map, err = pokeapi.GetMap(next_map)

	return err
}

func commandMapBack() error {
	if prev_map == "" {
		fmt.Println("You're on the first page")
		return nil
	}

	var err error
	next_map, prev_map, err = pokeapi.GetMap(prev_map)

	return err
}
