from functools import lru_cache
from typing import Sequence

from sentence_transformers import SentenceTransformer


MODEL_NAME = "Qwen/Qwen3-Embedding-0.6B"
EMBEDDING_DIMENSION = 1024


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once per process, on first use."""
    return SentenceTransformer(MODEL_NAME)


def create_document_embeddings(
    documents: Sequence[str],
    *,
    batch_size: int = 4,
    show_progress_bar: bool = False,
) -> list[list[float]]:
    """Create normalized 1,024-dimensional vectors for recipe documents."""
    if not documents:
        return []
    if any(not document.strip() for document in documents):
        raise ValueError("Documents must contain non-whitespace text")

    embeddings = get_embedding_model().encode(
        list(documents),
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=show_progress_bar,
    )

    expected_shape = (len(documents), EMBEDDING_DIMENSION)
    if embeddings.shape != expected_shape:
        raise ValueError(
            f"Expected embedding shape {expected_shape}, got {embeddings.shape}"
        )

    return embeddings.tolist()
