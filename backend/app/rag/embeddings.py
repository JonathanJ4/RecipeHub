from sentence_transformers import SentenceTransformer


model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")


def embed_text(text:str) -> list[float]: 
    embeddings = model.encode(text)
    
    return embeddings.tolist() 

