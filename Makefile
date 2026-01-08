.PHONY: help install lint test run docs docs-serve docker-build docker-run docker-serve docker-schedule clean

# ==============================================================================
# Venv
# ==============================================================================

UV := $(shell command -v uv 2> /dev/null)
VENV_DIR?=.venv
PYTHON := $(VENV_DIR)/bin/python

# ==============================================================================
# Targets
# ==============================================================================

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install       Install dependencies"
	@echo "  lint          Run linter and type checker"
	@echo "  test          Run tests"
	@echo "  run           Run the CLI"
	@echo "  docs          Build documentation"
	@echo "  docs-serve    Serve documentation locally"
	@echo "  docker-build     Build Docker image"
	@echo "  docker-run       Run import in Docker"
	@echo "  docker-serve     Start API server in Docker"
	@echo "  docker-schedule  Start scheduler in Docker"
	@echo "  clean            Clean up temporary files"

install:
	@echo ">>> Installing dependencies"
	@$(UV) sync --all-extras

lint:
	@echo ">>> Running linter"
	@$(UV) run ruff format .
	@$(UV) run ruff check . --fix
	@echo ">>> Running type checker"
	@$(UV) run mypy .
	@$(UV) run pyright

test:
	@echo ">>> Running tests"
	@$(UV) run pytest -v

run:
	@$(UV) run dhis2-era5land

docs:
	@$(UV) run mkdocs build

docs-serve:
	@$(UV) run mkdocs serve

docker-build:
	@docker build -t dhis2-era5land .

docker-run:
	@docker run --env-file .env dhis2-era5land run

docker-serve:
	@docker run -p 8080:8080 --env-file .env dhis2-era5land serve

docker-schedule:
	@docker compose up schedule

clean:
	@echo ">>> Cleaning up"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .coverage htmlcov coverage.xml
	@rm -rf dist build *.egg-info site

# ==============================================================================
# Default
# ==============================================================================

.DEFAULT_GOAL := help
