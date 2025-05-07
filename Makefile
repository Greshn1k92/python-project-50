.PHONY: lint test install check test-coverage

install:
	pip install -e .

lint:
	python -m ruff check .

test:
	python -m pytest

test-coverage:
	python -m pytest --cov=gendiff --cov-report xml --junitxml=test-results.xml

check: lint test 