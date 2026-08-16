from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import database_is_available
from .routers.recipes import router as recipes_router


IMAGES_DIRECTORY = Path(__file__).resolve().parent.parent / "static" / "images"


app = FastAPI(
    title="Recipe Hub API",
    description="FastAPI backend for the Recipe Hub application.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins.split(","),
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
    except Exception:
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
