package pokeapi

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"

	"github.com/EricSchrock/boot-dev/pokedex/internal/pokecache"
)

type Areas struct {
	Count    int    `json:"count"`
	Next     string `json:"next"`
	Previous string `json:"previous"`
	Results  []struct {
		Name string `json:"name"`
		Url  string `json:"url"`
	} `json:"results"`
}

type Area struct {
	PokemonEncounters []struct {
		Pokemon struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"pokemon"`
	} `json:"pokemon_encounters"`
}

type Pokemon struct {
	Name           string `json:"name"`
	BaseExperience int    `json:"base_experience"`
}

func GetAreasURL() string {
	return "https://pokeapi.co/api/v2/location-area"
}

func getURL(url string, cache *pokecache.Cache) ([]byte, error) {
	body, exists := cache.Get(url)
	if !exists {
		res, err := http.Get(url)
		if err != nil {
			return nil, err
		}
		defer res.Body.Close()

		if res.StatusCode != http.StatusOK {
			return nil, fmt.Errorf("Status code: %v", res.StatusCode)
		}

		body, err = io.ReadAll(res.Body)
		if err != nil {
			return nil, err
		}

		cache.Add(url, body)
	}

	return body, nil
}

func GetAreas(url string, cache *pokecache.Cache) (Areas, error) {
	body, err := getURL(url, cache)
	if err != nil {
		return Areas{}, err
	}

	areas := Areas{}
	if err := json.Unmarshal(body, &areas); err != nil {
		return Areas{}, err
	}

	return areas, nil
}

func GetArea(location string, cache *pokecache.Cache) (Area, error) {
	url := GetAreasURL() + "/" + location
	body, err := getURL(url, cache)
	if err != nil {
		return Area{}, fmt.Errorf("Failed to get '%s': %v", location, err)
	}

	area := Area{}
	if err := json.Unmarshal(body, &area); err != nil {
		return Area{}, err
	}

	return area, nil
}

func GetPokemon(name string, cache *pokecache.Cache) (Pokemon, error) {
	url := "https://pokeapi.co/api/v2/pokemon/" + name
	body, err := getURL(url, cache)
	if err != nil {
		return Pokemon{}, fmt.Errorf("Failed to get '%s': %v", name, err)
	}

	pokemon := Pokemon{}
	if err := json.Unmarshal(body, &pokemon); err != nil {
		return Pokemon{}, err
	}

	return pokemon, nil
}
