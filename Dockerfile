FROM python:3.12-slim as builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends && apt-get install -y gettext

WORKDIR /code

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-cache
ENV PATH="/app/.venv/bin:$PATH"

COPY . .
