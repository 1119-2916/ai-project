.PHONY: requirements
requirements:
	poetry export --without-hashes --dev --output poetry-requirements.txt

.PHONY: install
install:
	poetry install

.PHONY: run
run:
	poetry run python -m discord_bot

.PHONY: generate_dataset
generate_dataset:
	poetry run python -m train_data_generator

.PHONY: validate_format
validate_format:
	poetry run python -m validate_format

.PHONY: upload
upload:
	poetry run python -m openai_setup upload

.PHONY: tuning
tuning:
	poetry run python -m openai_setup tuning

