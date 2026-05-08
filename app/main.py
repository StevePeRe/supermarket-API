import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.database import Base, engine, verify_database_connection

from app.auth.router import router as auth_router
from app.products.router import router as products_router
from app.orders.router import router as orders_router
from app.inventory.router import router as inventory_router
from app.reports.router import router as reports_router

from app.auth import models as auth_models
from app.products import models as product_models
from app.orders import models as order_models
from app.inventory import models as inventory_models

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    verify_database_connection()
    logger.info("Database connection OK")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created")
    yield


settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(products_router, prefix=settings.api_prefix)
app.include_router(orders_router, prefix=settings.api_prefix)
app.include_router(inventory_router, prefix=settings.api_prefix)
app.include_router(reports_router, prefix=settings.api_prefix)


@app.get("/health")
def health():
    return {"status": "ok"}
