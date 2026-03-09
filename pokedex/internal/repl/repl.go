package repl

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strings"
	"time"

	"github.com/EricSchrock/boot-dev/pokedex/internal/pokeapi"
	"github.com/EricSchrock/boot-dev/pokedex/internal/pokecache"
)

type config struct {
	nextAreaURL string
	prevAreaURL string
	cache       *pokecache.Cache
	pokedex     map[string]pokeapi.Pokemon
}

type cliCommand struct {
	description string
	callback    func(*config, ...string) error
}

func StartREPL() {
	cfg := &config{
		nextAreaURL: pokeapi.GetAreasURL(),
		prevAreaURL: "",
		cache:       pokecache.NewCache(5 * time.Second),
		pokedex:     make(map[string]pokeapi.Pokemon),
	}
	defer cfg.cache.Close()

	scanner := bufio.NewScanner(os.Stdin)

	for {
		fmt.Print("Pokedex > ")

		if !scanner.Scan() {
			if err := scanner.Err(); err != nil {
				fmt.Println("Error:", err)
			}
		}

		words := cleanInput(scanner.Text())
		if len(words) == 0 {
			fmt.Println("Empty command")
			continue
		}

		command := words[0]
		c, ok := getCommands()[command]
		if !ok {
			fmt.Println("Unknown command:", command)
			continue
		}

		args := []string{}
		if len(words) > 1 {
			args = words[1:]
		}

		err := c.callback(cfg, args...)
		if err != nil {
			fmt.Println("Error:", err)
		}
	}
}

func cleanInput(text string) []string {
	return strings.Fields(strings.ToLower(text))
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
		"explore": {
			description: "Lists the pokemon found at the provided location",
			callback:    commandExplore,
		},
		"catch": {
			description: "Attempt to catch a pokemon",
			callback:    commandCatch,
		},
	}
}

func commandExit(cfg *config, args ...string) error {
	fmt.Println("Closing the Pokedex... Goodbye!")
	os.Exit(0)
	return nil
}

func commandHelp(cfg *config, args ...string) error {
	fmt.Println("Welcome to the Pokedex!")
	fmt.Println("Usage:")
	fmt.Println()
	for k, v := range getCommands() {
		fmt.Printf("%-4s: %s\n", k, v.description)
	}
	return nil
}

func commandMapForward(cfg *config, args ...string) error {
	if cfg.nextAreaURL == "" {
		fmt.Println("You're on the last page")
		return nil
	}

	areas, err := pokeapi.GetAreas(cfg.nextAreaURL, cfg.cache)
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

func commandMapBack(cfg *config, args ...string) error {
	if cfg.prevAreaURL == "" {
		fmt.Println("You're on the first page")
		return nil
	}

	areas, err := pokeapi.GetAreas(cfg.prevAreaURL, cfg.cache)
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

func commandExplore(cfg *config, args ...string) error {
	if len(args) < 1 {
		return fmt.Errorf("You must provide a location to explore")
	}

	fmt.Printf("Exploring %s...\n", args[0])
	area, err := pokeapi.GetArea(args[0], cfg.cache)
	if err != nil {
		return err
	}

	for _, encounter := range area.PokemonEncounters {
		fmt.Println(encounter.Pokemon.Name)
	}

	return nil
}

func commandCatch(cfg *config, args ...string) error {
	if len(args) < 1 {
		return fmt.Errorf("You must provide a pokemon to catch")
	}

	fmt.Printf("Throwing a Pokeball at %s...\n", args[0])
	pokemon, err := pokeapi.GetPokemon(args[0], cfg.cache)
	if err != nil {
		return err
	}

	if rand := rand.Intn(pokemon.BaseExperience / 50); rand != 0 {
		fmt.Println(args[0], "escaped!")
		return nil
	}
	fmt.Println(args[0], "was caught!")
	cfg.pokedex[args[0]] = pokemon

	return nil
}
