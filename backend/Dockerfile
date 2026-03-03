ARG UV_VERSION=0.8.13

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

FROM python:3.12-slim-bookworm AS base

WORKDIR /code

ENV VIRTUAL_ENV="/venvs/.venv"
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"



FROM base AS build-lambda

COPY --from=uv /uv /uvx /bin/

ENV UV_PROJECT_ENVIRONMENT=${VIRTUAL_ENV} \
    UV_LINK_MODE=copy

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project --group lambda


FROM base AS lambda

COPY --from=build-lambda ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENV PYTHONDONTWRITEBYTECODE=1 \
    # Turns off buffering for easier container logging
    PYTHONUNBUFFERED=1 \
    PATH="${VIRTUAL_ENV}/bin:$PATH"

COPY ./app ./app
COPY ./templates ./templates

ENTRYPOINT [ "python", "-m", "awslambdaric" ]

CMD [ "app.main.handler" ]
