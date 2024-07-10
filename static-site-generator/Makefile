.PHONY: all
all:
	python src/main.py
	cd public && python3 -m http.server 8888

.PHONY: test
test:
	python -m unittest discover -s src
