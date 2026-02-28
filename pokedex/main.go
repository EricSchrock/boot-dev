package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	registerCommands()

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
		c, ok := commands[command]
		if !ok {
			fmt.Println("Unknown command:", command)
			continue
		}

		err := c.callback()
		if err != nil {
			fmt.Println("Error:", err)
		}
	}
}
