package main

import (
	"fmt"
)

func handleLogin(s *state, cmd command) error {
	if len(cmd.args) == 0 {
		return fmt.Errorf("Expected a username")
	} else if len(cmd.args) > 1 {
		return fmt.Errorf("Expected just a username but got other inputs as well")
	}

	if err := s.cfg.SetUser(cmd.args[0]); err != nil {
		return err
	}

	fmt.Printf("User set to '%v'\n", s.cfg.User)

	return nil
}
