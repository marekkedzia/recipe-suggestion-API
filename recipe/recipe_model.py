from pydantic import BaseModel


class RecipeModel(BaseModel):
    id: str
    name: str
    creator_username: str
    image_url: str
