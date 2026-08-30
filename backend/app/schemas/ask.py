from pydantic import BaseModel


class AskRequest(BaseModel):
    query: str
    conversation_id: str | None = None


class AskResponse(BaseModel):
    answer: str
    conversation_id: str
    
    model_config = {"from_attributes": True}