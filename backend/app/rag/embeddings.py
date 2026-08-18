from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

print("Embedding model loaded.")


def embed_text(texts:list[str]) -> list[list[float]]: 
    embeddings = model.encode(texts,batch_size=5)
    if embeddings.shape[1] != 1024:
        raise ValueError("Expected 1024-dimensional embeddings")
    
    return embeddings.tolist() 

