from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import SQLAlchemyError

from .config import settings
from .database import close_database, database_is_available
from .routers import recipes_router


IMAGES_DIRECTORY = Path(__file__).resolve().parent.parent / "static" / "images"


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await close_database()


app = FastAPI(
    title="Recipe Hub API",
    description="FastAPI backend for the Recipe Hub application.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipes_router)
app.mount("/images", StaticFiles(directory=IMAGES_DIRECTORY), name="images")


@app.get("/health", tags=["Health"])
async def health_check() -> JSONResponse:
    """Return API and PostgreSQL availability."""
    try:
        await database_is_available()
    except SQLAlchemyError:
        return JSONResponse(
            status_code=503,
            content={
                "status": "degraded",
                "service": "recipe-hub-api",
                "database": "offline",
            },
        )

    return JSONResponse(
        content={
            "status": "ok",
            "service": "recipe-hub-api",
            "database": "online",
        }
    )
