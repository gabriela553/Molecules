.PHONY: build test

build:
	docker-compose up -d --build
test: build
	@echo "Running tests..."
	python -m pytest -v -s
