.PHONY: docs
docs:
	@poetry run pydoc-markdown

.PHONY: install
install:
	@poetry install

.PHONY: install-dev
install-dev:
	@poetry install --with=dev

.PHONY: lint
lint:
	@poetry run ruff check src tests

.PHONY: lint-fix
lint-fix:
	@poetry run ruff check src tests --fix

.PHONY: test-integration
test-integration: install-dev
	@poetry run pytest --cov-report term-missing --cov=./src ./tests/integration

.PHONY: install-dev test-integration-multi-language
test-integration-multi-language:
	@poetry run tox

.PHONY: test-unit
test-unit: install-dev
	@poetry run pytest --cov-report term-missing --cov=./src ./tests/unit

.PHONY: prerelease
prerelease: test-unit test-integration-multi-language
	@rm -rf dist
	@poetry build

.PHONY: release
release: prerelease
	@poetry run twine upload dist/*
