.PHONY: test eval demo run-api

PYTHON ?= python3

test:
	$(PYTHON) -m unittest discover -s app/tests -p 'test_*.py'

eval:
	$(PYTHON) evals/run_evals.py

demo:
	$(PYTHON) scripts/run_local.py

run-api:
	$(PYTHON) -m app.api.main
