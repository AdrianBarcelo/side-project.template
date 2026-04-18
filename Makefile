#!/usr/bin/make -f

PROJECT_NAME := 'project'

.PHONY: install-test-requirements test linting build
.PHONY: env-start env-stop env-recreate docker-cleanup bash
.PHONY: migrations migrate migrations-downgrade

ROOT_FOLDER := $(shell pwd)
DOCKER_COMPOSE_FILE := $(ROOT_FOLDER)/docker/docker-compose.yml
DOCKER_PROJECT_NAME := project
DOCKER_COMMAND := docker-compose -p $(DOCKER_PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE)

ifeq ($(DOCKER_IMAGE_NAME),)
export DOCKER_IMAGE_NAME := project
endif

ifeq ($(DOCKER_IMAGE_TAG),)
export DOCKER_IMAGE_TAG := latest
endif

install-test-requirements: ## Install all test dependencies
	$(DOCKER_COMMAND) exec -T app pip install --disable-pip-version-check -r /app/requirements/test.txt

test: ## Run test suite
	$(DOCKER_COMMAND) exec -T app /app/scripts/test-command.sh

linting: ## Check code style (mypy + ruff + black)
	$(DOCKER_COMMAND) exec -T app /app/scripts/lint-command.sh $(LINTFLAGS)

me-happy: ## Auto-fix code style
	$(DOCKER_COMMAND) exec -T app /app/scripts/fix-command.sh

build: ## Build project image
	$(DOCKER_COMMAND) build --no-cache --pull

env-start: ## Start project containers
	$(DOCKER_COMMAND) up -d

env-stop: ## Stop project containers
	$(DOCKER_COMMAND) stop

env-restart: env-stop env-start ## Restart project containers

env-destroy: ## Destroy all project containers
	$(DOCKER_COMMAND) down -v --rmi all --remove-orphans

env-recreate: build env-start install-test-requirements ## Rebuild and restart containers

destroy-containers: ## Destroy project containers
	$(DOCKER_COMMAND) down -v

docker-cleanup: ## Purge all Docker images
	$(DOCKER_COMMAND) down -v
	docker system prune -f

bash: ## Open a bash shell in main container
	$(DOCKER_COMMAND) exec app bash

migrations: ## Create new alembic revision (use: make migrations m="description")
	$(DOCKER_COMMAND) exec app alembic revision --autogenerate -m "$(m)"

migrate: ## Apply pending migrations
	$(DOCKER_COMMAND) exec app alembic upgrade head

migrations-downgrade: ## Rollback last migration
	$(DOCKER_COMMAND) exec app alembic downgrade -1

view-logs: ## Show container logs
	$(DOCKER_COMMAND) logs -f

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
