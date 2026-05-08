# Supermarket API

REST API for supermarket order and inventory management built with FastAPI.

## Features

- **Auth** — JWT-based authentication with roles (admin, warehouse, delivery)
- **Products** — Product and category CRUD
- **Orders** — Order creation with line items and status transitions
- **Inventory** — Stock tracking with low-stock alerts
- **Reports** — Top-selling products and daily sales summary

## Tech Stack

- FastAPI + Uvicorn
- SQLAlchemy + PostgreSQL (SQLite for local dev)
- Docker + docker-compose
- JWT (python-jose)
- Redis (caching / Celery backend)

## Quick Start

```bash
# Copy env and edit as needed
cp .env.example .env

# Install dependencies
pip install uv
uv sync

# Run locally with SQLite
uv run uvicorn app.main:app --reload

# Run with Docker (PostgreSQL + Redis)
docker compose up --build
```

## API Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Tests

```bash
uv sync --group test
uv run pytest
```
