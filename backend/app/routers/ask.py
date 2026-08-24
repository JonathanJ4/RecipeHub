from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import Text, cast, or_, select

from ..database import async_session_factory
from ..models.recipe import Recipe
from ..schemas.ask import AskRequest,AskResponse


router = APIRouter(prefix="/recipes", tags=["Recipes"])

@router.post("/ask", response_model=[AskResponse()])
async def ask(request:AskRequest):
    
