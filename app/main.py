import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import init_db
from app.api.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("logs", exist_ok=True)
    setup_logging()
    await init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-step AI stock analysis API powered by Claude + Yahoo Finance",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
