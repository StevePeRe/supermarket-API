FROM python:3.13-slim AS builder

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir uv && uv sync --no-dev --frozen

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
