FROM python:3.12-alpine AS build

WORKDIR /code

# Poetry will not create a new virtual environment (to reduce container )
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \ 
    POETRY_VIRTUALENVS_OPTIONS_NO_PIP=true \
    # Ensure pipx is available in the PATH
    PATH="/root/.local/bin:$PATH"

# Install system dependencies and pipx
RUN python3 -m pip install --user pipx && \
    python3 -m pipx ensurepath && \
    # Install Poetry using pipx
    pipx install poetry


# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-interaction --no-ansi --only main

COPY ./app ./app


# Command for development
FROM build AS development

ENV PATH="/code/.venv/bin:${PATH}"

CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0"]


# Commands for production
FROM python:3.12-alpine AS production

WORKDIR /code

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1 \
    # Turns off buffering for easier container logging
    PYTHONUNBUFFERED=1 \
    # Disable pip cache
    PIP_NO_CACHE_DIR=1 \
    PATH="/code/.venv/bin:${PATH}"


COPY --from=build /code /code

# Run the FastAPI application
CMD ["fastapi", "run", "--workers", "4", "app/main.py"]

