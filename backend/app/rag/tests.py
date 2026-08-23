from .embeddings import embed_queries
from ..database import async_session_factory
from sqlalchemy import select
from ..models.recipe import Recipe
import asyncio

async def testingembeddings():
        query  = "What can I make with chicken and brocolli"
        embeded_query = embed_queries(query)
        
        async with async_session_factory() as session:
                result = await session.scalars(
                            select(Recipe.title)
                            .where(Recipe.embedding.is_not(None))
                            .order_by(Recipe.embedding.cosine_distance(embeded_query))
                            .limit(5)
                        )
        print(result.all())
        return result.all()
        
  


if __name__ == "__main__":
    asyncio.run(testingembeddings())  