ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION} as base

RUN apt-get update && apt-get -y install \
    build-essential \
    libssl-dev \
    libffi-dev \
    cargo \
    pkg-config


FROM base as test

COPY . /src
WORKDIR /src
RUN pip install -r requirements/development.txt

# Used to force the cache to bust before running the tests when desired
ARG RUN_ID=test

RUN pytest -v
