PYTHON = python3
NAME = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean lint build

run:
	$(PYTHON) $(NAME) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(NAME) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info

install:
	$(PYTHON) -m pip install flake8 mypy build "setuptools>=61" wheel

lint:
	flake8 --exclude=.git,.venv,__pycache__,build,dist,*.egg-info .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

build:
	$(PYTHON) -m build --no-isolation
