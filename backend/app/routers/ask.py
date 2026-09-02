from ..rag.generation import generation
from ..schemas.ask import AskRequest, AskResponse
from fastapi import APIRouter

router = APIRouter(tags=["Ask"])

@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    answer, conversation_id = await generation(
        request.query,
        request.conversation_id,
    )
    
    return {
        "answer": answer,
        "conversation_id": conversation_id,
    }
