.PHONY: requirements
requirements:
	poetry export --without-hashes --dev --output poetry-requirements.txt

.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run python -m bot