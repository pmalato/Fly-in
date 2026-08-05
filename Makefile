LFLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
VENV = ./fly-in.venv/bin

all: run

run:
	$(VENV)/python3 fly-in.py

install:
	test -d fly-in.venv || python3 -m venv fly-in.venv
	$(VENV)/pip install -r requirements.txt


debug:
	$(VENV)/python3 pdb -m fly-in.py

clean:
	rm -fr .mypy_cache
	rm -fr src/.mypy_cache
	rm -fr src/__pycache__
	clear

lint:
	python3 -m flake8 .
	python3 -m mypy . $(LFLAGS)

lint-strict:
	python3 -m flake8 .
	python3 -m mypy --strict .

.PHONY: all run install debug clean lint lint-strict