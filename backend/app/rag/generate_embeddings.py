from .embeddings import embed_text
from ..database import async_session_factory
from ..models.recipe import Recipe
from sqlalchemy import select 
import asyncio



    
async def generate_embeddings():
    async with async_session_factory() as session:
        result = await session.scalars(
                    select(Recipe)
                    .where(Recipe.embedding.is_(None))
                    .order_by(Recipe.id)
                    
                )
        recipes= result.all()
        texts = []
        for recipe in recipes:
            text = f"{recipe.title} {recipe.ingredients} {recipe.instructions}"            
            texts.append(text)
        
            
        embeddings = embed_text(texts)

        for recipe, embedding in zip(recipes, embeddings):
            recipe.embedding = embedding
            
        await session.commit()

if __name__ == "__main__":
    asyncio.run(generate_embeddings())