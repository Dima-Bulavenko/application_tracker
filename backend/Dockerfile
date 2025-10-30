FROM python:3.12-slim-bookworm AS base

WORKDIR /code

ENV VIRTUAL_ENV="/venvs/.venv"

RUN python3 -m venv ${VIRTUAL_ENV}



FROM base AS build

ENV POETRY_NO_INTERACTION=1 \
    # restrict poetry create .venv in project directory
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    # make sure that poetry will create virtual environment
    POETRY_VIRTUALENVS_CREATE=0 \
    # don't install pip in new .venv
    POETRY_VIRTUALENVS_OPTIONS_NO_PIP=1 \
    # change directory where poetry stores cache
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    # change path where poetry store its .venv
    POETRY_VIRTUALENVS_PATH=${VIRTUAL_ENV} \
    # Ensure pipx is available in the PATH
    PATH="/root/.local/bin:$PATH"

# Install system dependencies and pipx
RUN python3 -m pip install --user pipx && \
    python3 -m pipx ensurepath && \
    # Install Poetry using pipx
    pipx install poetry==1.8.4

ENV PATH="${VIRTUAL_ENV}/bin:$PATH"

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-interaction --no-ansi --no-root --only main



# Commands for production
FROM base AS production

COPY --from=build ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1 \
    # Turns off buffering for easier container logging
    PYTHONUNBUFFERED=1 \
    PATH="${VIRTUAL_ENV}/bin:$PATH"

COPY ./app ./app
# Run the FastAPI application
CMD ["fastapi", "run", "--workers", "4", "app/main.py"]



FROM production AS lambda

ENTRYPOINT [ "python", "-m", "awslambdaric" ]

CMD [ "app.main.handler" ]
