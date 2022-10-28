FROM python:3.10

WORKDIR /code

# Install poetry:
RUN pip install poetry

# Disable virtualenv creation:
RUN poetry config virtualenvs.create false

# Copy requirements:
COPY ./pyproject.toml ./poetry.lock* /code/

# Copy credentials
COPY ./credentials /code/credentials

# Install deps:
RUN poetry install --no-root

COPY ./app /code/app