import random

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from food_data_provider.cuisine_type import CuisineType
from food_data_provider.diet_types import DietType
from recipe.recipe_model import RecipeModel
from recipe.recipe_service import RecipeService
from utils.pagination import Pagination
from utils.response_bodies import ResponseBody
from food_data_provider.course_types import CourseType


def main():
    recipe_service = RecipeService()
    router = APIRouter()

    @router.get("/recipe/{recipe_id}/pdf")
    async def get_recipe_in_pdf(recipe_id: str):
        file = await recipe_service.generate_pdf(recipe_id)
        return StreamingResponse(file, media_type="application/pdf")

    @router.get("/recipe/random")
    async def get_random_recipe(page: int, page_size: int):
        default_max_ready_time = 180
        return await recipe_service.get_recipes(
            {
                "page": page,
                "page_size": page_size,
                "maxReadyTime": default_max_ready_time,
                "type": random.choice(list(CourseType)),
                "diet": None,
                "cuisine": None
            }
        )

    @router.get("/recipe")
    async def get_recipe_option(
            page: int,
            page_size: int,
            max_ready_time: int = None,
            course_type: CourseType = None,
            diet_type: DietType = None,
            cuisine: CuisineType = None,
            description: str = None,
    ):
        return await recipe_service.get_recipes(
            {
                "page": page,
                "page_size": page_size,
                "query": description,
                "maxReadyTime": max_ready_time,
                "type": course_type,
                "diet": diet_type,
                "cuisine": cuisine
            }
        )

    @router.get("/recipe/{recipe_id}")
    async def get_recipe_option_information(recipe_id: str):
        return await recipe_service.get_recipe(recipe_id)

    @router.post("/recipe", status_code=201)
    async def save_recipe(recipe: RecipeModel):
        await recipe_service.save_recipe(recipe.dict())
        return ResponseBody.CREATED

    @router.get("/saved-recipe")
    async def get_recipes(page: int, page_size: int):
        return await recipe_service.get_saved_recipes(Pagination(page, page_size))

    return router
