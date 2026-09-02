from ..rag.retrieval import retrieval
from ..rag.generation import generation
from ..schemas.ask import AskRequest, AskResponse
from fastapi import APIRouter

router = APIRouter(tags=["Ask"])

@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    answer = await generation(request.query)
    
    return {
        "answer": answer,
    }
