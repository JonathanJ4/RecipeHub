from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

print("Embedding model loaded.")


def embed_text(text:str) -> list[float]: 
    embeddings = model.encode(text)
    
    return embeddings.tolist() 

