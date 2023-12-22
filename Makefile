format:
	poetry run scripts/run_formatters.sh
test:
	poetry run scripts/run_unit_tests.sh
lint:
	poetry run scripts/run_linters.sh
build:
	bash scripts/build.sh
run_sample:
	bash scripts/run_sample_app.sh