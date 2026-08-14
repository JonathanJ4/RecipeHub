from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import Text, cast, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_database_session
from ..models import Recipe
from ..schemas import RecipeResponse


router = APIRouter(prefix="/recipes", tags=["Recipes"])
DatabaseSession = Annotated[AsyncSession, Depends(get_database_session)]


@router.get("", response_model=list[RecipeResponse])
async def get_recipes(
    session: DatabaseSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Recipe]:
    """Return recipes in stable ID order with offset pagination."""
    result = await session.scalars(
        select(Recipe)
        .order_by(Recipe.id)
        .offset(offset)
        .limit(limit)
    )
    return list(result)


@router.get("/search", response_model=list[RecipeResponse])
async def search_recipes(
    session: DatabaseSession,
    q: Annotated[str, Query(min_length=1, max_length=200)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Recipe]:
    """Search recipe titles, instructions, and ingredient text."""
    query = q.strip()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Search query cannot be blank.",
        )

    search_filter = or_(
        Recipe.title.icontains(query, autoescape=True),
        Recipe.instructions.icontains(query, autoescape=True),
        cast(Recipe.ingredients, Text).icontains(query, autoescape=True),
    )
    result = await session.scalars(
        select(Recipe)
        .where(search_filter)
        .order_by(Recipe.id)
        .offset(offset)
        .limit(limit)
    )
    return list(result)


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe_by_id(
    recipe_id: int,
    session: DatabaseSession,
) -> Recipe:
    """Return one recipe or a 404 response when it does not exist."""
    recipe = await session.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found.",
        )
    return recipe
