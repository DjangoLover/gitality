.PHONY: requirements settings sqlite

PROJECT_NAME = gitality
PROJECT_VIRTUALENV = $(WORKON_HOME)/$(PROJECT_NAME)
PROJECT_ROOT = $(PROJECT_NAME)
PROJECT_CORE = $(PROJECT_ROOT)/$(PROJECT_NAME)
DEPLOY_DIR = deploy
FIXTURES_DIR = fixtures

PIP = $(PROJECT_VIRTUALENV)/bin/pip
PYTHON = $(PROJECT_VIRTUALENV)/bin/python
DJANGO = $(PYTHON) $(PROJECT_ROOT)/manage.py

BS=\033[1m
BE=\033[0m
BSU=\033[1;4m
BLUE=\033[34m
CYAN=\033[36m
GREEN=\033[32m
MAGENTA=\033[35m
RED=\033[31m
WHITE=\033[1;37m
YELLOW=\033[33m
PREFIX=$(BS)=>$(BE)$(WHITE)


default: bootstrap prepare db end

bootstrap:
	@echo $(ECHO_OPTIONS) "$(BLUE)$(PREFIX) Running bootstrap.sh script for virtual environment preparation"
	@./$(DEPLOY_DIR)/bootstrap.sh

prepare: settings requirements

settings:
	@echo "$(BLUE)$(PREFIX) Emitting local settings module$(BE)"
	@cp $(DEPLOY_DIR)/local_settings_dev.py $(PROJECT_CORE)/local_settings.py

requirements:
	@echo "$(BLUE)$(PREFIX) Installing requirements$(BE)"
	@$(PIP) install -qr requirements.txt -U

scrapy_requirements:
	@echo "$(BLUE)$(PREFIX) Installing Scrapy requirements$(BE)"
	@$(PIP) install -qr scripts/scraper/requirements.txt -U

db: syncdb migrate seed

syncdb:
	@echo "$(BLUE)$(PREFIX) Syncing database and loading initial fixtures$(BE)"
	@$(DJANGO) syncdb --noinput -v 0

migrate:
	@echo "$(BLUE)$(PREFIX) Running migrations$(BE)"
	@$(DJANGO) migrate --noinput -v 0

seed:
	@echo "$(BLUE)$(PREFIX) Seeding database with additional fixtures$(BE)"
	@$(DJANGO) loaddata -v 0 $(FIXTURES_DIR)/dev/*
	@$(DJANGO) loaddata -v 0 $(FIXTURES_DIR)/common/*

end:
	@echo "$(BLUE)$(PREFIX) Project environment is ready. You can run it using $(MAGENTA)make run$(WHITE).$(BE)"

createsuperuser:
	@$(DJANGO) createsuperuser

run:
	@$(DJANGO) runserver

shell:
	@$(DJANGO) shell

freeze:
	@echo "$(BLUE)$(PREFIX) Creating or updating requirements file$(BE)"
	@$(PIP) freeze > requirements.txt
	@echo "$(GREEN)$(PREFIX) Requirements file is ready and stored in $(MAGENTA)requirements.txt$(WHITE)$(BE)"

requirements_upgrade:
	@echo "$(BLUE)$(PREFIX) $(YELLOW)Upgrading requirements$(WHITE)$(BE)"
	@$(PIP) freeze | cut -d = -f 1 | xargs $(PIP) install -Uq
	@$(MAKE) freeze

clean:
	@echo "$(BLUE)$(PREFIX) $(YELLOW)Cleaning up bytecode$(WHITE)$(BE)"
	@find . -name '*.pyc' -exec rm -f {} \;

settings_postgres:
	@echo "$(BLUE)$(PREFIX) Emitting local settings module (with PostgreSQL support)$(BE)"
	@cp $(DEPLOY_DIR)/local_settings_dev_postgres.py $(PROJECT_CORE)/local_settings.py


postgres: dropdb createdb

createdb:
	@echo "$(BLUE)$(PREFIX) Creating PostgreSQL database $(GREEN)$(PROJECT_NAME)$(WHITE)$(BE)"
	@createdb $(PROJECT_NAME) | true

dropdb:
	@echo "$(BLUE)$(PREFIX) Destroying PostgreSQL database $(GREEN)$(PROJECT_NAME)$(WHITE)$(BE)"
	@dropdb $(PROJECT_NAME) | true

db_production: postgres syncdb migrate seed_production

settings_production:
	@echo "$(BLUE)$(PREFIX) Emitting local settings module for production environment$(BE)"
	@cp $(DEPLOY_DIR)/local_settings_prod.py $(PROJECT_CORE)/local_settings.py

seed_production:
	@echo "$(BLUE)$(PREFIX) Seeding database with additional fixtures for production environment$(BE)"
	@$(DJANGO) loaddata -v 0 $(FIXTURES_DIR)/prod/*
	@$(DJANGO) loaddata -v 0 $(FIXTURES_DIR)/common/*

collectstatic:
	@echo "$(BLUE)$(PREFIX) Collecting static files$(BE)"
	@$(DJANGO) collectstatic -v 0 --noinput

test:
	@$(DJANGO) test --settings=gitality.settings_test

fakemigrations:
	@echo "$(BLUE)$(PREFIX) Running fake migrations$(BE)"
	@$(DJANGO) migrate achievements 0001 --fake
	@$(DJANGO) migrate commits 0001 --fake
	@$(DJANGO) migrate core 0001 --fake

celery:
	@$(DJANGO) celery worker -B
