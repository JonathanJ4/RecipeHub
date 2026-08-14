import argparse
import ast
import asyncio
import csv
from pathlib import Path

from sqlalchemy import func, insert, select

from app.database import async_session_factory, close_database
from app.models import Recipe


DEFAULT_CSV_PATH = Path(__file__).resolve().parents[2] / "data" / "kaggle" / "recipes.csv"
BATCH_SIZE = 250


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import recipes from the CSV dataset.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV_PATH,
        help="Path to the recipe CSV file.",
    )
    return parser.parse_args()


def read_recipes(csv_path: Path) -> tuple[list[dict], int]:
    recipes: list[dict] = []
    skipped = 0

    with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        required_columns = {"Title", "Ingredients", "Instructions", "Image_Name"}
        missing_columns = required_columns.difference(reader.fieldnames or [])
        if missing_columns:
            names = ", ".join(sorted(missing_columns))
            raise ValueError(f"CSV is missing required columns: {names}")

        for row_number, row in enumerate(reader, start=2):
            title = row["Title"].strip()
            instructions = row["Instructions"].strip()
            image_name = row["Image_Name"].strip()

            if not title or not instructions or not image_name:
                skipped += 1
                continue

            try:
                ingredients = ast.literal_eval(row["Ingredients"])
            except (SyntaxError, ValueError) as error:
                raise ValueError(
                    f"Invalid Ingredients list on CSV row {row_number}"
                ) from error

            if not isinstance(ingredients, list):
                raise ValueError(
                    f"Ingredients must be a list on CSV row {row_number}"
                )

            recipes.append(
                {
                    "title": title,
                    "ingredients": ingredients,
                    "instructions": instructions,
                    "image_name": image_name,
                    "image_url": None,
                }
            )

    return recipes, skipped


async def import_recipes(recipes: list[dict]) -> None:
    async with async_session_factory() as session:
        async with session.begin():
            existing_count = await session.scalar(
                select(func.count()).select_from(Recipe)
            )
            if existing_count:
                raise RuntimeError(
                    f"Import aborted: recipes already contains {existing_count} rows."
                )

            for start in range(0, len(recipes), BATCH_SIZE):
                batch = recipes[start : start + BATCH_SIZE]
                await session.execute(insert(Recipe), batch)


async def main() -> None:
    arguments = parse_arguments()
    recipes, skipped = read_recipes(arguments.csv.resolve())

    try:
        await import_recipes(recipes)
    finally:
        await close_database()

    print(f"Imported {len(recipes):,} recipes.")
    print(f"Skipped {skipped:,} incomplete rows.")


if __name__ == "__main__":
    asyncio.run(main())
