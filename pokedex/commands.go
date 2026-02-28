package main

import (
	"fmt"
	"os"

	"github.com/EricSchrock/boot-dev/pokedex/internal/pokeapi"
)

type config struct {
	nextAreaURL string
	prevAreaURL string
}

type cliCommand struct {
	description string
	callback    func(*config) error
}

func getCommands() map[string]cliCommand {
	return map[string]cliCommand{
		"exit": {
			description: "Exit the Pokedex",
		callback:    commandExit,
		},
		"help": {
			description: "Displays a help message",
		callback:    commandHelp,
		},
		"map": {
			description: "Displays the next 20 map locations",
		callback:    commandMapForward,
		},
		"mapb": {
			description: "Displays the last 20 map locations",
		callback:    commandMapBack,
		},
	}
}

func commandExit(cfg *config) error {
	fmt.Println("Closing the Pokedex... Goodbye!")
	os.Exit(0)
	return nil
}

func commandHelp(cfg *config) error {
	fmt.Println("Welcome to the Pokedex!")
	fmt.Println("Usage:")
	fmt.Println()
	for k, v := range getCommands() {
		fmt.Printf("%-4s: %s\n", k, v.description)
	}
	return nil
}

func commandMapForward(cfg *config) error {
	if cfg.nextAreaURL == "" {
		fmt.Println("You're on the last page")
		return nil
	}

	areas, err := pokeapi.GetAreas(cfg.nextAreaURL)
	if err != nil {
		return err
	}

	for _, area := range areas.Results {
		fmt.Println(area.Name)
	}

	cfg.nextAreaURL = areas.Next
	cfg.prevAreaURL = areas.Previous

	return nil
}

func commandMapBack(cfg *config) error {
	if cfg.prevAreaURL == "" {
		fmt.Println("You're on the first page")
		return nil
	}

	areas, err := pokeapi.GetAreas(cfg.prevAreaURL)
	if err != nil {
		return err
	}

	for _, area := range areas.Results {
		fmt.Println(area.Name)
	}

	cfg.nextAreaURL = areas.Next
	cfg.prevAreaURL = areas.Previous

	return nil
}
