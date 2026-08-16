import argparse
import asyncio
from collections.abc import Sequence

from sqlalchemy import select, update

from app.database import async_session_factory, close_database
from app.models import Recipe
from app.rag.embeddings import create_document_embeddings


DEFAULT_LIMIT = 15


def positive_integer(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Qwen embeddings for recipes without an embedding."
    )
    parser.add_argument(
        "--limit",
        type=positive_integer,
        default=DEFAULT_LIMIT,
        help=f"Maximum recipes to process (default: {DEFAULT_LIMIT}).",
    )
    parser.add_argument(
        "--batch-size",
        type=positive_integer,
        default=4,
        help="Number of recipe documents embedded together (default: 4).",
    )
    return parser.parse_args()


def build_recipe_document(recipe: Recipe) -> str:
    """Combine the searchable recipe fields into one labeled string."""
    ingredients = ", ".join(str(item) for item in recipe.ingredients)
    return (
        f"Title: {recipe.title}\n"
        f"Ingredients: {ingredients}\n"
        f"Instructions: {recipe.instructions}"
    )


async def load_recipes(limit: int) -> Sequence[Recipe]:
    async with async_session_factory() as session:
        result = await session.scalars(
            select(Recipe)
            .where(Recipe.embedding.is_(None))
            .order_by(Recipe.id)
            .limit(limit)
        )
        return result.all()


async def save_embeddings(
    recipe_ids: Sequence[int], embeddings: Sequence[Sequence[float]]
) -> None:
    async with async_session_factory.begin() as session:
        for recipe_id, embedding in zip(recipe_ids, embeddings, strict=True):
            await session.execute(
                update(Recipe)
                .where(Recipe.id == recipe_id, Recipe.embedding.is_(None))
                .values(embedding=list(embedding))
            )


async def generate_embeddings(limit: int, batch_size: int) -> int:
    recipes = await load_recipes(limit)
    if not recipes:
        return 0

    documents = [build_recipe_document(recipe) for recipe in recipes]
    embeddings = await asyncio.to_thread(
        create_document_embeddings,
        documents,
        batch_size=batch_size,
        show_progress_bar=True,
    )
    await save_embeddings([recipe.id for recipe in recipes], embeddings)
    return len(recipes)


async def main() -> None:
    arguments = parse_arguments()
    try:
        generated_count = await generate_embeddings(
            limit=arguments.limit,
            batch_size=arguments.batch_size,
        )
    finally:
        await close_database()

    print(f"Stored embeddings for {generated_count} recipes.")


if __name__ == "__main__":
    asyncio.run(main())
