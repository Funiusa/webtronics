FROM python:3.10-slim-bookworm

LABEL authors="Denis"

EXPOSE 8000

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update -qq \
    && DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
        apt-transport-https \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        gnupg \
        jq \
        less \
        libpcre3 \
        libpcre3-dev \
        openssh-client \
        telnet \
        unzip \
        vim \
        wget \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && truncate -s 0 /var/log/*log

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=$HOME/.poetry/ python3 -

ENV PATH $PATH:/root/.poetry/bin

RUN poetry config virtualenvs.create false

RUN mkdir -p /app/poetry

WORKDIR /app

COPY sonet/ app/
COPY sonet/poetry/pyproject.toml ./poetry/

RUN poetry install -C poetry --no-interaction --no-ansi