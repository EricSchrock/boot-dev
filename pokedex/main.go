package main

import (
	"bufio"
	"fmt"
	"os"

	"github.com/EricSchrock/boot-dev/pokedex/internal/pokeapi"
)

func main() {
	cfg := &config{
		nextAreaURL: pokeapi.GetAreasURL(),
		prevAreaURL: "",
	}

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

		err := c.callback(cfg)
		if err != nil {
			fmt.Println("Error:", err)
		}
	}
}
