from ..database import async_session_factory
from embeddings import embed_text
from models import Recipe
from sqlalchemy import Text, cast, or_, select
from sqlalchemy import Text, cast, or_, select


limit= 5
async def generate_embeddings():
    async with async_session_factory() as session:
        result = await session.scalars(
                    select(Recipe)
                    .order_by(Recipe.id)
                    .limit(limit)
                ).all()
        text=""
        for recipe in result:
            text += f"{recipe.title} {recipe.ingredients} {recipe.instructions}"            
            embed_text(text)
    