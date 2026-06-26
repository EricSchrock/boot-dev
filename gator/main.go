package main

import (
	"log"
	"os"

	"github.com/EricSchrock/boot-dev/gator/internal/config"
	"github.com/EricSchrock/boot-dev/gator/internal/state"
)

func main() {
	cfg, err := config.Read()
	if err != nil {
		log.Fatalf("Error reading config: %v", err)
	}

	var s state.State
	s.Config = &cfg

	cmds := commands{
		handlers: make(map[string]func(*state.State, command) error),
	}

	cmds.register("login", handleLogin)

	if len(os.Args) < 2 {
		log.Fatalf("No command provided")
	}

	cmd := command{
		name: os.Args[1],
		args: os.Args[2:],
	}

	err = cmds.run(&s, cmd)
	if err != nil {
		log.Fatalf("Error running '%v' command: %v", cmd.name, err)
	}
}
