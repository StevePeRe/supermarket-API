# Supermarket API
REST API for supermarket order and inventory management built with FastAPI.
## Features
- **Auth** — JWT-based authentication with roles (admin, warehouse, delivery)
- **Products** — Product and category CRUD
- **Orders** — Order creation with line items and status transitions
- **Inventory** — Stock tracking with low-stock alerts
- **Reports** — Top-selling products and daily sales summary
## Tech Stack
- **Framework**: FastAPI + Uvicorn (async)
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL (production) / SQLite (development)
- **Migrations**: Alembic
- **Auth**: JWT (python-jose) + bcrypt
- **Cache**: Redis (prepared)
- **Tasks**: Celery (prepared)
## Project Structure (Hexagonal Architecture)
```
app/
├── domain/                 # Business logic (no dependencies)
│   ├── entities/           # Pure data classes
│   └── repositories/       # Repository interfaces (ports)
├── application/            # Use cases
│   ├── commands/           # Write operations (CQRS)
│   ├── queries/            # Read operations (CQRS)
│   └── dtos/               # Data transfer objects
└── infrastructure/         # External implementations
    ├── api/                # HTTP routes & dependencies
    ├── auth/               # JWT & password handling
    ├── config/             # Settings
    └── persistence/        # SQLAlchemy models & repos
```
## Quick Start
```bash
# Install dependencies
uv sync
# Run database migrations (first time)
uv run alembic upgrade head
# Start development server
uv run uvicorn app.main:app --reload
# Or with Docker (PostgreSQL + Redis)
docker compose up --build
```
## Database Migrations (Alembic)
```bash
# Create new migration
uv run alembic revision --autogenerate -m "description"
# Apply migrations
uv run alembic upgrade head
# Rollback last migration
uv run alembic downgrade -1
# Show migration history
uv run alembic history
```
## Tests
```bash
# Run all tests with coverage
uv run pytest --cov=app --cov-report=term-missing
# Run only unit tests
uv run pytest tests/unit/
# Run only integration tests
uv run pytest tests/integration/
```
## API Documentation
| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/auth/register` | POST | Public | Register user |
| `/api/v1/auth/login` | POST | Public | Login |
| `/api/v1/products` | GET | Public | List products |
| `/api/v1/products` | POST | warehouse/admin | Create product |
| `/api/v1/orders` | GET | Auth | List my orders |
| `/api/v1/orders` | POST | Auth | Create order |
| `/api/v1/inventory` | GET | warehouse/admin | View inventory |
| `/api/v1/inventory/alerts` | GET | warehouse/admin | Low stock alerts |
| `/api/v1/reports/top-products` | GET | admin | Top selling |
| `/api/v1/reports/daily-summary` | GET | admin | Daily summary |
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
## User Roles
| Role | Permissions |
|------|-------------|
| `admin` | Full access |
| `warehouse` | Products & inventory management |
| `delivery` | Prepared for future use |
## Environment Variables
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/supermarket
USE_POSTGRES=false
JWT_SECRET_KEY=change-me-in-production
REDIS_URL=redis://localhost:6379/0
```
