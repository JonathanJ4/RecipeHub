from pydantic import BaseModel
from .recipe import RecipeResponse

class AskRequest(BaseModel):
    query: str


class AskResponse(BaseModel):
    answer: str
    recipes: list[RecipeResponse]