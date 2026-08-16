from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import Text, cast, or_, select

from ..database import async_session_factory
from ..models.recipe import Recipe
from ..schemas.recipe import RecipeResponse


router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get("", response_model=list[RecipeResponse])
async def get_recipes(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[Recipe]:
    """Return recipes in stable ID order with offset pagination."""
    async with async_session_factory() as session:
        result = await session.scalars(
            select(Recipe)
            .order_by(Recipe.id)
            .offset(offset)
            .limit(limit)
        )
        return list(result)


@router.get("/search", response_model=list[RecipeResponse])
async def search_recipes(
    q: str = Query(..., min_length=1, max_length=200),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[Recipe]:
    """Search recipe titles, instructions, and ingredient text."""
    query = q.strip()
    if not query:
        raise HTTPException(
            status_code=422,
            detail="Search query cannot be blank.",
        )

    search_filter = or_(
        Recipe.title.icontains(query, autoescape=True),
        Recipe.instructions.icontains(query, autoescape=True),
        cast(Recipe.ingredients, Text).icontains(query, autoescape=True),
    )
    async with async_session_factory() as session:
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
) -> Recipe:
    """Return one recipe or a 404 response when it does not exist."""
    async with async_session_factory() as session:
        recipe = await session.get(Recipe, recipe_id)
        if recipe is None:
            raise HTTPException(
                status_code=404,
                detail="Recipe not found.",
            )
        return recipe
