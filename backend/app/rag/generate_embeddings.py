import asyncio
import json

from sqlalchemy import select

from app.database import async_session_factory, close_database
from app.models import Recipe
from app.rag.embeddings import create_embeddings


TEST_LIMIT = 15


def recipe_to_text(recipe: Recipe) -> str:
    """Build the text that represents a recipe for semantic search."""
    ingredients = json.dumps(recipe.ingredients, ensure_ascii=False)
    return (
        f"Title: {recipe.title}\n"
        f"Ingredients: {ingredients}\n"
        f"Instructions: {recipe.instructions}"
    )


async def generate_embeddings(limit: int = TEST_LIMIT) -> None:
    """Generate and save embeddings for a small number of unprocessed recipes."""
    async with async_session_factory() as session:
        result = await session.execute(
            select(Recipe)
            .where(Recipe.embedding.is_(None))
            .order_by(Recipe.id)
            .limit(limit)
        )
        recipes = result.scalars().all()

        if not recipes:
            print("No recipes without embeddings were found.")
            return

        for number, recipe in enumerate(recipes, start=1):
            recipe.embedding = await create_embeddings(recipe_to_text(recipe))
            print(f"Embedded {number}/{len(recipes)}: {recipe.title}")

        await session.commit()
        print(f"Saved {len(recipes)} recipe embeddings.")


async def main() -> None:
    try:
        await generate_embeddings()
    finally:
        await close_database()


if __name__ == "__main__":
    asyncio.run(main())
