PYTHON = python3
MAP ?= maps/easy/01_linear_path.txt

.PHONY: install run visualize debug clean lint lint-strict

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) main.py "$(MAP)"

visualize:
	$(PYTHON) main.py "$(MAP)" --gui

debug:
	$(PYTHON) -m pdb main.py "$(MAP)"

clean:
	find . -type d \( -name .venv -o -name .git -o -name .local \) -prune -o -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict
