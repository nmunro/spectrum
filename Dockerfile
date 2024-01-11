FROM python:3.11 as DEV
# Configure Poetry

ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.7.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

WORKDIR /app/resourcedb
# Install poetry separated from system interpreter

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools wheel \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

COPY . /app/resourcedb
RUN poetry install && poetry lock && poetry export -f requirements.txt --output requirements.txt
RUN groupadd -r docker && useradd -r -m -g docker docker
RUN chown -R docker /opt
ENV PYTHONPATH $PYTHONPATH:/app

FROM python:3.11 as PROD

ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_VERSION=1.7.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

WORKDIR /app/resourcedb
RUN apt update -y && apt upgrade -y

COPY . /app/resourcedb
COPY --from=dev /app/resourcedb/requirements.txt .

RUN pip install -r requirements.txt
RUN groupadd -r docker && useradd -r -m -g docker docker

