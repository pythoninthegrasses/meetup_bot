# syntax=docker/dockerfile:1.17.1
# check=skip=all

# full semver just for python base image
ARG PYTHON_VERSION=3.11.13

FROM python:${PYTHON_VERSION}-slim-bookworm as builder

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# install dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get -qq update \
  && apt-get -qq install \
  --no-install-recommends -y \
  curl \
  gcc \
  python3-dev

# venv
ARG UV_PROJECT_ENVIRONMENT="/opt/venv"
ENV VENV="${UV_PROJECT_ENVIRONMENT}"
ENV PATH="$VENV/bin:$PATH"

# uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY ./app .
COPY ./README.md .
COPY pyproject.toml .

# optimize startup time, don't use hardlinks, set cache for buildkit mount,
# set uv timeout
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_CACHE_DIR=/opt/uv-cache/
ENV UV_HTTP_TIMEOUT=90

RUN --mount=type=cache,target=/opt/uv-cache,sharing=locked \
  uv venv $UV_PROJECT_ENVIRONMENT \
  && uv pip install -r pyproject.toml

FROM python:${PYTHON_VERSION}-slim-bookworm as runner

# set timezone
ENV TZ=${TZ:-"America/Chicago"}
RUN ln -snf "/usr/share/zoneinfo/${TZ}" /etc/localtime && echo "$TZ" > /etc/timezone

# setup standard non-root user for use downstream
ENV USER_NAME=appuser
ARG VENV="/opt/venv"
ENV PATH=$VENV/bin:$HOME/.local/bin:$PATH

# standardise on locale, don't generate .pyc, enable tracebacks on seg faults
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# workers per core
# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/blob/master/README.md#web_concurrency
ENV WEB_CONCURRENCY=2

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# install dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get -qq update \
  && apt-get -qq install \
  --no-install-recommends -y \
  curl \
  lsof

# add non-root user
ARG UID=10001
RUN adduser \
  --disabled-password \
  --gecos "" \
  --home "/nonexistent" \
  --shell "/sbin/nologin" \
  --no-create-home \
  --uid "${UID}" \
  ${USER_NAME}

RUN mkdir -p /data && chown 10001:10001 /data

USER ${USER_NAME}

WORKDIR /app

COPY --chown=${USER_NAME} ./app .
COPY --from=builder --chown=${USER_NAME} "$VENV" "$VENV"

ARG PORT=${PORT:-3000}
EXPOSE $PORT

CMD ["/bin/sh", "startup.sh"]

LABEL org.opencontainers.image.title="meetup_bot"
LABEL org.opencontainers.image.version="latest"
