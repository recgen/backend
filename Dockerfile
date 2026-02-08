FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV UV_NO_DEV=1 \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

COPY ./uv.lock ./pyproject.toml /app/
RUN uv sync --locked --no-install-project

COPY . /app/
RUN uv sync --locked

EXPOSE 8080

ENV GROUP=app-group \
    USER=app-user

RUN groupadd $GROUP &&\
    useradd -g $GROUP $USER -m

USER $USER

ENV UV_NO_SYNC=1

# CMD uv run alembic upgrade head && \
#     uv run api

CMD uv run api
