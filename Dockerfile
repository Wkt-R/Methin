# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/src

WORKDIR /app

RUN useradd --create-home --uid 1000 methin

COPY requirements.txt .
RUN pip install -r requirements.txt

# --- dev: zależności testowe/lintery, kod montowany wolumenem ---
FROM base AS dev
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt
COPY pyproject.toml ./
COPY src ./src
COPY tests ./tests
USER methin
CMD ["python", "-m", "methin"]

# --- prod: tylko to, co potrzebne do działania ---
FROM base AS prod
COPY src ./src
USER methin
CMD ["python", "-m", "methin"]
