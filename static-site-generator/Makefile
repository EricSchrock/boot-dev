.PHONY: all
all:
	python src/main.py

.PHONY: test
test:
	python -m unittest discover -s src

.PHONY: server
server:
	python server.py --dir public
