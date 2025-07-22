# VARIABLE DEFINITIONS
venv := ".venv"
python_version :="3.13"
run := "poetry run"
eval_path := "eval/cli.py"

venv-exists := path_exists(venv)


target_dirs := "src tests eval"

# ALIASES
alias t := test
help:
    just --list --unsorted

# Cleans all artifacts generated while running this project, including the virtualenv.
venv: 
    @if ! {{ venv-exists }}; \
    then \
    uv sync --frozen --all-extras; \
    fi

# Runs the evaluation script
eval *args: venv
    PYTHONPATH=. {{ run }} python {{ eval_path }} {{ args }}

# Cleans all artifacts generated while running this project, including the virtualenv.
clean: 
    @rm -f .coverage*
    @rm -rf {{ venv }}

# Runs the tests with the specified arguments (any path or pytest argument).
test *test-args='': venv
    {{ run }}  pytest {{ test-args }} --no-cov 

# Runs all tests including coverage report.
test-all: venv
    {{ run }}  pytest

# Format all code in the project.
format:  venv
    {{ run }} ruff check {{ target_dirs }}

# Lint all code in the project.
lint: venv
    {{ run }}  ruff check {{ target_dirs }}
    {{ run }}  mypy {{ target_dirs }}
