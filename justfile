# VARIABLE DEFINITIONS
venv := ".venv"
python_version :="3.13"

venv-exists := path_exists(venv)


target_dirs := "src tests"

# ALIASES
alias t := test
help:
    just --list --unsorted

# Cleans all artifacts generated while running this project, including the virtualenv.
venv: 
    @if ! {{ venv-exists }}; \
    then \
    uv sync --all-extras; \
    fi


# Cleans all artifacts generated while running this project, including the virtualenv.
clean: 
    @rm -f .coverage*
    @rm -rf {{ venv }}

# Runs the tests with the specified arguments (any path or pytest argument).
test *test-args='': venv
    uv run pytest {{ test-args }} --no-cov 

# Runs all tests including coverage report.
test-all: venv
    uv run pytest

# Format all code in the project.
format:  venv
    uv run ruff check {{ target_dirs }} --fix

# Lint all code in the project.
lint: venv
    uv run ruff check {{ target_dirs }}
    uv run mypy {{ target_dirs }}
