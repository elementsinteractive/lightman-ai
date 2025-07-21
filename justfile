# VARIABLE DEFINITIONS
venv := ".venv"
python_version :="3.13"


target_dirs := "src tests"

# ALIASES
alias t := test
help:
    just --list --unsorted

# Cleans all artifacts generated while running this project, including the virtualenv.
venv: 
    @uv sync --group test --group lint --group local


# Cleans all artifacts generated while running this project, including the virtualenv.
clean:
    @rm -f .coverage*
    @rm -rf {{ venv }}

# Runs the tests with the specified arguments (any path or pytest argument).
test *test-args='': 
    uv run pytest {{ test-args }} --no-cov 

# Runs all tests including coverage report.
test-all: 
    uv run pytest

# Format all code in the project.
format:  
    uv run ruff check {{ target_dirs }} --fix

# Lint all code in the project.
lint: 
    uv run ruff check {{ target_dirs }}
    uv run mypy {{ target_dirs }}

