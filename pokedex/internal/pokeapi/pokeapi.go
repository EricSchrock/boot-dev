package pokeapi

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type Areas struct {
	Count    int    `json:count`
	Next     string `json:next`
	Previous string `json:previous`
	Results  []struct {
		Name string `json:name`
		Url  string `json:url`
	} `json:results`
}

func GetAreasURL() string {
	return "https://pokeapi.co/api/v2/location-area"
}

func GetAreas(url string) (Areas, error) {
	res, err := http.Get(url)
	if err != nil {
		return Areas{}, err
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		return Areas{}, fmt.Errorf("Status code: %v", res.StatusCode)
	}

	body, err := io.ReadAll(res.Body)
	if err != nil {
		return Areas{}, err
	}

	areas := Areas{}
	if err := json.Unmarshal(body, &areas); err != nil {
		return Areas{}, err
	}

	return areas, nil
}
