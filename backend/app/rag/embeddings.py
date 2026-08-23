from sentence_transformers import SentenceTransformer
import sys
import torch

print("PYTHON:", sys.executable)
print("TORCH:", torch.__version__)
print("TORCH PATH:", torch.__file__)
print("CUDA:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "NONE")

print("Loading embedding model...")

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B",device="cuda")

print("Embedding model loaded.")


def embed_text(texts:list[str]) -> list[list[float]]: 
    embeddings = model.encode(texts,batch_size=5,show_progress_bar=True,)
    if embeddings.shape[1] != 1024:
        raise ValueError("Expected 1024-dimensional embeddings")
    
    return embeddings.tolist() 

def embed_queries(query:str) -> list[float]:
    embedding = model.encode(
        [query],
        prompt_name="query",
    )

    return embedding[0].tolist()