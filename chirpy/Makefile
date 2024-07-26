.PHONY: all
all: build run

.PHONY: build
build:
	go fmt
	go build -o server

.PHONY: run
run:
	./server

.PHONY: test
test:
	curl --header "Content-Type: application/json" --request POST --data '{"body":"hello world"}' localhost:8080/api/validate_chirp
	curl --header "Content-Type: application/json" --request POST --data '{"body":"hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world hello world"}' localhost:8080/api/validate_chirp
