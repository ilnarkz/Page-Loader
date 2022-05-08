install:
	poetry install
lint:
	poetry run flake8 pageloader
test:
	poetry run pytest
selfcheck:
	poetry check
check: selfcheck test lint
test-coverage:
	poetry run pytest --cov=pageloader --cov-report xml tests/
build:
	rm -rf dist
	poetry build
package-install:
	pip install --user dist/*.whl
