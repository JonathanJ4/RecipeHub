from .embeddings import embed_text
from ..database import async_session_factory
from ..models.recipe import Recipe
from sqlalchemy import select

limit= 5
async def generate_embeddings():
    async with async_session_factory() as session:
        result = await session.scalars(
                    select(Recipe)
                    .order_by(Recipe.id)
                    .limit(limit)
                )
        recipes= result.all()
        
        for recipe in recipes:
            text=""
            text += f"{recipe.title} {recipe.ingredients} {recipe.instructions}"            
            recipe.embedding = embed_text(text)
            
        
        await session.commit()
    