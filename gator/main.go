package main

import (
	"log"
	"os"

	"github.com/EricSchrock/boot-dev/gator/internal/commands"
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

	cmds := &commands.Commands{
		Handlers: make(map[string]func(*state.State, commands.Command) error),
	}

	cmds.Register("login", handleLogin)

	if len(os.Args) < 2 {
		log.Fatalf("No command provided")
	}

	cmd := commands.Command{
		Name: os.Args[1],
		Args: os.Args[2:],
	}

	err = cmds.Run(&s, cmd)
	if err != nil {
		log.Fatalf("Error running '%v' command: %v", cmd.Name, err)
	}
}
