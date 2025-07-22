ARG PYTHON_IMAGE=3.13-slim

# --------------- `base` stage --------------- 
FROM python:${PYTHON_IMAGE} AS base

# Define global values. Define them as ARG so they are not present in the final image, and so they can be modified
ARG USER=lightman
ARG GROUP=lightman
ARG WORKDIR=/app
ARG VENV_PATH=${WORKDIR}/.venv
ARG BIN_PATH=${VENV_PATH}/bin

WORKDIR ${WORKDIR}

# Create a non-root user and group
RUN groupadd -g 1001 ${GROUP} && \
    useradd -m -u 1001 -g ${GROUP} -s /bin/false ${USER}

# --------------- `build` stage --------------- 
FROM base AS build

# Define stage variables
ARG UV_VERSION 0.8.0
# Install curl for uv installation
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Copy dependency files
COPY uv.lock pyproject.toml ./

# Install dependencies using uv (only dependencies, not the project itself)
RUN UV_PROJECT_ENVIRONMENT=${VENV_PATH} uv sync --frozen --no-install-project --compile-bytecode
RUN ${BIN_PATH}/python -m ensurepip
# --------------- `final` stage --------------- 
FROM base AS final

# Set non-root user and group
USER ${USER}:${GROUP}

# Copy the virtual environment from build stage 
COPY --from=build --chown=${USER}:${GROUP} ${VENV_PATH} ${VENV_PATH}

# Set PATH to use the virtual environment
ENV PATH="${BIN_PATH}:$PATH"

# Copy pyproject.toml for package metadata
COPY --from=build --chown=${USER}:${GROUP} ${WORKDIR}/pyproject.toml .

COPY README.md README.md
# Copy source code
COPY src src

# Install the CLI tool (dependencies already installed in venv)
RUN ${BIN_PATH}/pip3 install --no-deps .

ENTRYPOINT [ "lightman-ai" ]
