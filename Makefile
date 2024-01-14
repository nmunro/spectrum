.PHONY: build clean clean-docker clean-docs docs repl test shell start stop lint migrate migrations dev-tools-check lint-tools-check logs static poetry create-super-user restart
.DEFAULT_GOAL: build

REPORT := $(or $(REPORT),report -m)
GIT_CHANGED_PYTHON_FILES := $(shell git diff --name-only -- '***.py')
LINTING_TOOLS := $(and $(shell which black),$(shell which isort),$(shell which flake8))
DEV_TOOLS := $(and $(shell which docker git))
COMPOSE_FILE := 'docker-compose.yml'
RUNNING_CONTAINERS := $(shell docker ps -a -q -f name="neurodb-*")
SERVICE := $(or $(SERVICE),web-dev)

# define standard colors
ifneq ($(TERM),)
    GREEN        := $(shell tput setaf 2)
    RESET        := $(shell tput sgr0)

else
    GREEN        := ""
    RESET        := ""

endif

dev-tools-check:
ifeq ($(DEV_TOOLS),)
	$(error Some of your dev tools are missing, unable to proceed)
endif

lint-tools-check:
ifeq ($(LINTING_TOOLS),)
	$(error Some of your linting tools are missing, unable to proceed)
endif

build: dev-tools-check
ifeq ($(FORCE),true)
	@docker container rm -f $(SERVICE)
	@docker container prune
endif
	@docker compose -f $(COMPOSE_FILE) build $(SERVICE)

start: dev-tools-check
	@docker compose -f $(COMPOSE_FILE) up $(SERVICE) -d --remove-orphans

stop: dev-tools-check
	@docker compose -f $(COMPOSE_FILE) down $(SERVICE)

restart: stop start

lint: lint-tools-check
	@$(foreach file, $(GIT_CHANGED_PYTHON_FILES), $(shell black ${file}; isort ${file}; flake8 ${file}))

static: dev-tools-check
	@docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) poetry run python manage.py collectstatic

migrate: dev-tools-check
	@docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) poetry run python manage.py migrate

migrations: dev-tools-check
	@docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) poetry run python manage.py makemigrations $(ARGS)

repl: dev-tools-check
	@docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) poetry run python manage.py shell

shell:
	@docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) /bin/bash

test: dev-tools-check
	@rm -rf coverage
ifneq ($(and $(TEST-CASE),$(SRC)),)
	@docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) coverage run --source=$(SRC) --branch ./manage.py test --no-input $(TEST-CASE); docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) coverage $(REPORT)
else ifneq ($(SRC),)
	@docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) coverage run --source=$(SRC) --branch ./manage.py test --no-input; docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) coverage $(REPORT)
else ifneq ($(TEST-CASE),)
	@docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) coverage run --branch ./manage.py test --no-input $(TEST-CASE) --parallel
else
	@docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) coverage run --branch ./manage.py test --no-input --parallel
endif
	@rm -rf .coverage.*

clean:
	@docker container prune -f

ifeq ($(IMAGES),true)
	@docker image prune -fa
	@docker builder prune -fa
endif

ifeq ($(VOLUMES),true)
	@docker volume prune -fa
endif

ifeq ($(SYSTEM),true)
	@docker system prune -fa
	@docker builder prune -fa
endif

logs:
	@docker compose -f $(COMPOSE_FILE) logs -f $(SERVICE)

poetry:
ifeq ($(SERVICE),web)
	@docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) poetry $(CMD)
else
	$(error Command not available for service: '$(SERVICE)')
endif

create-super-user:
	@docker compose -f $(COMPOSE_FILE) run --rm $(SERVICE) poetry run python manage.py createsuperuser
