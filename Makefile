.PHONY: build run development

build:
	docker build -t python-test-img .

run:
	docker run -t --rm -v $(shell pwd):/tool/ --workdir /tool python-test-img python -m pytest -v

development:
	docker run -it --rm -v $(shell pwd):/tool/ --workdir /tool python-test-img