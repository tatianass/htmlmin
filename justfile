#!/usr/bin/env just --justfile

default:
  @just --list

# Initialize the local environment
init PY_VERSION='3.13':
    uv venv --python {{PY_VERSION}}
    uv tool install ruff
    uv tool install bandit
    pre-commit install

# Update the precommit
update:
    pre-commit autoupdate

# Delete all temporary files
clean:
    rm -rf .ipynb_checkpoints
    rm -rf **/.ipynb_checkpoints
    rm -rf .pytest_cache
    rm -rf **/.pytest_cache
    rm -rf __pycache__
    rm -rf **/__pycache__
    rm -rf build
    rm -rf dist

# Install for production
install:
    uv sync

# Generate requirements
compile:
	uv pip compile pyproject.toml -o requirements.txt

# Format files using ruff
format:
    uv tool run ruff check --fix
    uv tool run ruff format

# Run tests
test:
    uv run pytest --cov=src --log-level=WARNING --disable-pytest-warnings --junitxml=junit.xml -o junit_family=legacy

# Run pre-commit hooks without commiting
pre-commit:
    pre-commit run --all-files

alias fix := pre-commit
