from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecipeResponse(BaseModel):
    id: int
    title: str
    ingredients: list[str]
    instructions: str
    image_name: str
    image_url: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
