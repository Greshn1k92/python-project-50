.PHONY: lint test install check test-coverage

install:
	pip install -e .

lint:
	python -m ruff check .

test:
	pytest

test-coverage:
	pytest --cov=gendiff --cov-report xml --junitxml=test-results.xml

check: lint test 