package pokeapi

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type Areas struct {
	Count    int      `json:count`
	Next     string   `json:next`
	Previous string   `json:previous`
	Results  [20]Area `json:results`
}

type Area struct {
	Name string `json:name`
	Url  string `json:url`
}

func GetMap(link string) (string, string, error) {
	res, err := http.Get(link)
	if err != nil {
		return "", "", err
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		return "", "", fmt.Errorf("Status code: %v", res.StatusCode)
	}

	body, err := io.ReadAll(res.Body)
	if err != nil {
		return "", "", err
	}

	areas := Areas{}
	if err := json.Unmarshal(body, &areas); err != nil {
		return "", "", err
	}

	for _, area := range areas.Results {
		fmt.Println(area.Name)
	}

	return areas.Next, areas.Previous, nil
}
