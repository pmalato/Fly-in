export UV_CACHE_DIR := $(HOME)/sgoinfre/pecoelho/.cache/uv
export HF_HOME := &(HOME)/sgoinfre/pecoelho/.cache/hugginface

LFLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

all: run

run:
	uv run python3 fly-in.py $(ARGS)

install:
	uv sync

debug:
	uv run python3 pdb -m fly-in.py

clean:
	rm -fr .mypy_cache
	rm -fr src/.mypy_cache
	rm -fr src/__pycache__
	clear

fclean:
	rm -fr .venv/
	make clean

lint:
	uv run python3 -m flake8 .
	uv run python3 -m mypy . $(LFLAGS)

lint-strict:
	uv run python3 -m flake8 .
	uv run python3 -m mypy --strict .

.PHONY: all run install debug clean fclean lint lint-strict