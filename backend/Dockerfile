FROM python:3.12-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1 \
# Turns off buffering for easier container logging
    PYTHONUNBUFFERED=1 \
# Disable pip cache
    PIP_NO_CACHE_DIR=1

# Poetry will not create a new virtual environment (to reduce container )
ENV POETRY_VIRTUALENVS_CREATE=false

# Install system dependencies and pipx
RUN python3 -m pip install --user pipx && \
    python3 -m pipx ensurepath

# Ensure pipx is available in the PATH
ENV PATH="/root/.local/bin:$PATH"

# Install Poetry using pipx
RUN pipx install poetry

WORKDIR /code

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-interaction --no-ansi

# Copy application code
COPY ./app ./app

# Run the FastAPI application
CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--proxy-headers", "--port", "80"]