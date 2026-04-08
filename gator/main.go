package main

import (
	"fmt"
	"log"

	"github.com/EricSchrock/boot-dev/gator/internal/config"
)

func main() {
	c, err := config.Read()
	if err != nil {
		log.Fatalf("Error reading config: %v", err)
	}

	err = c.SetUser("eric")
	if err != nil {
		log.Fatalf("Error setting user: %v", err)
	}

	c, err = config.Read()
	if err != nil {
		log.Fatalf("Error reading back config: %v", err)
	}

	fmt.Println(c)
}
