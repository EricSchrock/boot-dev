package main

import (
	"bufio"
	"fmt"
	"os"
)

type cliCommand struct {
	name        string
	description string
	callback    func() error
}

var commands = map[string]cliCommand{}

func main() {
	commands["exit"] = cliCommand{
		name: "exit",
		description: "Exit the Pokedex",
		callback: commandExit,
	}

	commands["help"] = cliCommand{
		name: "exit",
		description: "Displays a help message",
		callback: commandHelp,
	}

	scanner := bufio.NewScanner(os.Stdin)

	for {
		fmt.Print("Pokedex > ")

		if scanner.Scan() {
			words := cleanInput(scanner.Text())
			if len(words) == 0 {
				continue
			}

			if c, ok := commands[words[0]]; ok {
				c.callback()
			} else {
				fmt.Println("Unknown command")
			}
		}

		if err := scanner.Err(); err != nil {
			fmt.Errorf("Error:", err)
		}
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
		fmt.Printf("%s: %s\n", k, v.description)
	}
	return nil
}
