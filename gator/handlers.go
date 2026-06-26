package main

import (
	"fmt"

	"github.com/EricSchrock/boot-dev/gator/internal/commands"
	"github.com/EricSchrock/boot-dev/gator/internal/state"
)

func handleLogin(s *state.State, cmd commands.Command) error {
	if len(cmd.Args) == 0 {
		return fmt.Errorf("Expected a username")
	} else if len(cmd.Args) > 1 {
		return fmt.Errorf("Expected just a username but got other inputs as well")
	}

	if err := s.Config.SetUser(cmd.Args[0]); err != nil {
		return err
	}

	fmt.Printf("User set to '%v'\n", s.Config.User)

	return nil
}
