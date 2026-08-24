from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import Text, cast, or_, select

from ..database import async_session_factory
from ..models.recipe import Recipe
from ..schemas.recipe import RecipeResponse


router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.get("/ask")