from pydantic import BaseModel


class AskRequest(BaseModel):
    query: str


class AskResponse(BaseModel):
    answer: str
    
    
    model_config = {"from_attributes": True}