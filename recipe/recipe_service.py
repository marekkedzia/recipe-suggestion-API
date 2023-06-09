from functools import partial
from cache_service.cache_service import CacheService
from cache_service.utils import convert_dict_to_key
from food_data_provider.food_api import FoodApi
from pdf_converter.converter import generate_pdf_file
from recipe.recipe_repository import RecipeRepository
from utils.pagination import Pagination


class RecipeService:

    def __init__(self):
        self.food_api_provider = FoodApi()
        self.recipe_repository = RecipeRepository()
        self.cache_service = CacheService()

    async def save_recipe(self, recipe: dict):
        await self.recipe_repository.insert_one(recipe)

    async def get_saved_recipes(self, pagination: Pagination):
        return await self.recipe_repository.get_recipes(pagination)

    async def get_recipe(self, option_id: str):
        return await self.cache_service.get(
            option_id,
            partial(
                self.food_api_provider.get_recipe_information,
                option_id
            ))

    async def get_recipes(self, params: dict):
        return await self.cache_service.get(
            convert_dict_to_key(params),
            partial(self.food_api_provider.get_recipe_options, params, Pagination(params["page"], params["page_size"])))

    async def generate_pdf(self, recipe_id):
        option_info = await self.get_recipe(option_id=recipe_id)
        return generate_pdf_file(option_info)
