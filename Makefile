install:
	poetry install
lint:
	poetry run flake8 page_loader
test:
	poetry run pytest
selfcheck:
	poetry check
check: selfcheck test lint
test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml tests/
build:
	rm -rf dist
	poetry build
package-install:
	pip install --user dist/*.whl
