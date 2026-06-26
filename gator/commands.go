package main

import (
	"fmt"

	"github.com/EricSchrock/boot-dev/gator/internal/state"
)

type command struct {
	name string
	args []string
}

type commands struct {
	handlers map[string]func(*state.State, command) error
}

func (c *commands) register(name string, f func(*state.State, command) error) {
	c.handlers[name] = f
}

func (c *commands) run(s *state.State, cmd command) error {
	handler, ok := c.handlers[cmd.name]
	if !ok {
		return fmt.Errorf("Invalid command: %v", cmd.name)
	}

	return handler(s, cmd)
}
