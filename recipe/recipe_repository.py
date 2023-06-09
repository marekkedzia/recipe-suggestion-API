import asyncio
from utils.database import get_recipe_collection
from utils.pagination import Pagination


class RecipeRepository:
    @staticmethod
    async def insert_one(recipe: dict):
        recipe_collection = await get_recipe_collection()
        await recipe_collection.insert_one(recipe)

    @staticmethod
    async def get_recipes(pagination: Pagination):
        recipe_collection = await get_recipe_collection()
        cursor = recipe_collection.find().skip(pagination.range_from).limit(pagination.range_to)
        recipes = await cursor.to_list(None)
        return await RecipeRepository.__serialize_list(recipes)

    @staticmethod
    async def __serialize_list(recipes):
        async def serialize(recipe):
            return {
                'id': recipe["id"],
                'name': recipe["name"],
                'creator_username': recipe["creator_username"],
                'image_url': recipe["image_url"]
            }

        serialized_recipes = await asyncio.gather(*[serialize(recipe) for recipe in recipes])
        return list(reversed(serialized_recipes))
