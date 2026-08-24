from .embeddings import embed_queries
from ..database import async_session_factory
from sqlalchemy import select
from ..models.recipe import Recipe
import asyncio
import requests 

 




                
                
query  = "What can I make with chicken and brocolli"            

async def testingembeddings():
        
        embeded_query = embed_queries(query)
        
        async with async_session_factory() as session:
                result = await session.scalars(
                            select(Recipe.title)
                            .where(Recipe.embedding.is_not(None))
                            .order_by(Recipe.embedding.cosine_distance(embeded_query))
                            .limit(5)
                        )
        
        return result.all()
        



async def get_response():
        base_url =  "http://127.0.0.1:1234/api/v1/chat"

        headers = {
                "Content-Type": "application/json"
}

        body = {
        "model": "qwen/qwen3-8b",
        "input": [
                {
                        "type":"text",
                        "content":f"""  

                                Retrieved chunks: {await testingembeddings()}
                                User_query: {query}     
                        """
                }
        ],
        "system_prompt": "Answer the users question using the retrieved content"
}
        response = requests.post(
                base_url,
                headers=headers,
                json=body
        )
        print(response.text)

if __name__ == "__main__":
    asyncio.run(get_response()) 