.PHONY: test run

test:
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests

run:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m aether
