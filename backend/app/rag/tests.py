from .embeddings import embed_text
from ..database import async_session_factory
from sqlalchemy import select
from ..models.recipe import Recipe

async def testingembeddings():
        query  = " chicken"
        embeded_query = embed_text(query)[0]
        
        async with async_session_factory() as session:
                result = await session.scalars(
                            select(Recipe.title)
                            .where(Recipe.embedding.is_not(None))
                            .order_by(Recipe.embedding.cosine_distance(embeded_query))
                            .limit(5)
                        )
        
    