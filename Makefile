install:
	uv sync
build:
	uv build
lint:
	uv run ruff check gendiff
gendiff:
	uv run gendiff
test:
	uv run pytest
test-coverage:
	uv run pytest --cov=gendiff --cov-report=xml
check:
	make lint
	make test
