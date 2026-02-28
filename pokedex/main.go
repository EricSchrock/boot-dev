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
