from .embeddings import embed_queries
from ..database import async_session_factory
from sqlalchemy import select
from ..models.recipe import Recipe


async def testingembeddings():
        
        embeded_query = embed_queries(query)
        
        async with async_session_factory() as session:
                result = await session.scalars(
                            select(Recipe)
                            .where(Recipe.embedding.is_not(None))
                            .order_by(Recipe.embedding.cosine_distance(embeded_query))
                            .limit(5)
                        )
        
        return result.all()
        