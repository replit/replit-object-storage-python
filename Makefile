.PHONY: install
install:
	@poetry install

.PHONY: lint
lint:
	@poetry run ruff check src tests

.PHONY: lint-fix
lint-fix:
	@poetry run ruff check src tests --fix

.PHONY: test-unit
test-unit:
	@poetry run pytest --cov-report term-missing --cov=./src ./tests/unit

.PHONY: prerelease
prerelease:
	@rm -rf dist
	@poetry build

.PHONY: release
release: prerelease
	@poetry run twine upload dist/*