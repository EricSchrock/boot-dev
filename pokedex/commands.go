package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

type cliCommand struct {
	description string
	callback    func() error
}

var commands = map[string]cliCommand{}

func registerCommands() {
	commands["exit"] = cliCommand{
		description: "Exit the Pokedex",
		callback: commandExit,
	}

	commands["help"] = cliCommand{
		description: "Displays a help message",
		callback: commandHelp,
	}

	commands["map"] = cliCommand{
		description: "Displays the next 20 map locations",
		callback: commandMap,
	}

	commands["mapb"] = cliCommand{
		description: "Displays the last 20 map locations",
		callback: commandMapBack,
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

type Areas struct {
	Count int `json:count`
	Next string `json:next`
	Previous string `json:previous`
	Results [20]Area `json:results`
}

type Area struct {
	Name string `json:name`
	Url string `json:url`
}

func commandMap() error {
	if next_map == "" {
		fmt.Println("You're on the last page")
		return nil
	}

	return getMap(next_map)
}

func commandMapBack() error {
	if prev_map == "" {
		fmt.Println("You're on the first page")
		return nil
	}

	return getMap(prev_map)
}

func getMap(link string) error {
	res, err := http.Get(link)
	if err != nil {
		return err
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("Status code: %v", res.StatusCode)
	}

	body, err := io.ReadAll(res.Body)
	if err != nil {
		return err
	}

	areas := Areas{}
	if err := json.Unmarshal(body, &areas); err != nil {
		return err
	}

	next_map = areas.Next
	prev_map = areas.Previous

	for _, area := range areas.Results {
		fmt.Println(area.Name)
	}

	return nil
}
