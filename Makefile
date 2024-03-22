SHELL := /usr/bin/env bash -o errtrace -o pipefail -o noclobber -o errexit -o nounset
.DEFAULT_GOAL := help

SOURCES ?= app
PROJECT_CONFIG ?= pyproject.toml

IMAGE_NAME ?= todo-app:$(shell whoami)

.PHONY: help
help: ## Display this help screen
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z._-]+:.*?## / {printf "\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

####################################################################################################
# Linters
####################################################################################################

.PHONY: format
format: ## Format the source code
	poetry run black $(SOURCES)
	poetry run isort $(SOURCES)

.PHONY: lint.bandit
lint.bandit:
	poetry run bandit -c $(PROJECT_CONFIG) -r $(SOURCES)

.PHONY: lint.mypy
lint.mypy:
	poetry run mypy --pretty $(SOURCES)

.PHONY: lint.refurb
lint.refurb:
	poetry run refurb $(SOURCES)

.PHONY: lint.flake8
lint.flake8:
	poetry run flake8 $(SOURCES)

.PHONY: lint.xenon
lint.xenon:
	@# xenon is not configurable by itself
	source /dev/stdin <<<"$$(grep xenon_ $(PROJECT_CONFIG)|tr -d ' ')" \
		&& poetry run xenon -e $${xenon_exclude} -b $${xenon_max_absolute} -m $${xenon_max_modules} -a $${xenon_max_average} $(SOURCES)

.PHONY: lint.isort
lint.isort:
	poetry run isort --check-only --diff $(SOURCES)

.PHONY: lint.black
lint.black:
	poetry run black --check --diff $(SOURCES)

.PHONY: lint
lint: lint.bandit lint.mypy lint.refurb lint.flake8 lint.xenon lint.isort lint.black ## Lint the source code

####################################################################################################
# Build
####################################################################################################

.PHONY: install
install: ## Install project dependencies
	poetry lock
	poetry install

.PHONY: dev.install
dev.install: ## Install dev project dependencies
	poetry lock
	poetry install --with dev

.PHONY: build
build: ## Build the docker image
	docker build -t $(IMAGE_NAME) $(ARGS) .

####################################################################################################
# Run
####################################################################################################

.PHONY: run
run: ## Run the project
	poetry run uvicorn app.main:app --reload

.PHONY: dev.up
dev.run: build ## Run in docker container detached
	docker run -d -p 8000:8000 $(IMAGE_NAME)
