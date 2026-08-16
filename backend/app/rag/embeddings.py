from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

async def create_embeddings(text:str)-> list[float]:
    embedding = await model.encode(text)
    
    if len(embedding)!= 1024:
        raise ValueError(f"Expected 1024 dimension received {len(embedding)}")
    
    return embedding


    