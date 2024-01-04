.PHONY: requirements
requirements:
	poetry export --without-hashes --dev --output poetry-requirements.txt

.PHONY: install
install:
	poetry install

# ex) make run KEY=meu
.PHONY: run
run:
	poetry run python -m discord_bot $(KEY)

.PHONY: run_kurobara
run_kurobara:
	poetry run python -m discord_bot kurobara

.PHONY: run_ikeda
run_ikeda:
	poetry run python -m discord_bot ikeda

.PHONY: generate_dataset
generate_dataset:
	poetry run python -m train_data_generator

.PHONY: validate_format
validate_format:
	poetry run python -m validate_format

# ex) make upload KEY=meu
.PHONY: upload
upload:
	poetry run python -m openai_setup upload $(KEY)

.PHONY: tuning
tuning:
	poetry run python -m openai_setup tuning $(KEY)

