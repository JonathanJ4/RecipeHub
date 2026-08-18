from .embeddings import embed_text
from ..database import async_session_factory
from ..models.recipe import Recipe
from sqlalchemy import select
import asyncio



    
    
LIMIT = 25
async def generate_embeddings():
    async with async_session_factory() as session:
        result = await session.scalars(
                    select(Recipe)
                    .order_by(Recipe.id)
                    .limit(LIMIT)
                )
        recipes= result.all()
        
        for recipe in recipes:
            text = f"{recipe.title} {recipe.ingredients} {recipe.instructions}"            
            recipe.embedding = embed_text(text)
            
        
        await session.commit()

if __name__ == "__main__":
    asyncio.run(generate_embeddings())