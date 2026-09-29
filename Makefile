.PHONY: install install-dev test lint format build run clean help
help: ## Show commands
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'
install: ## Install package
	python -m pip install .
install-dev: ## Install package and development tools
	python -m pip install -e '.[dev]'
test: ## Run tests
	pytest
lint: ## Run Ruff
	ruff check .
format: ## Format Python
	ruff format .
build: ## Build package
	python -m build
run: ## Show CLI help
	python -m gh_cleaner --help
clean: ## Remove build artifacts
	rm -rf build dist *.egg-info .pytest_cache .coverage
