import requests

from utils.config_envs import FOOD_API_URL, FOOD_API_KEY
from utils.pagination import Pagination


class FoodApi:
    def get_recipe_options(self, search_params: dict, pagination: Pagination):
        empty_param = ""
        instruction_policy = "true"
        url = f"{FOOD_API_URL}/recipes/complexSearch"

        search_params_keys = search_params.keys()
        params = {
            key: search_params.get(key, empty_param) for key in search_params_keys
        }

        params.update(
            {
                "apiKey": FOOD_API_KEY,
                "offset": pagination.range_from,
                "number": pagination.size,
                "instructionsRequired": instruction_policy,
            }
        )

        response = requests.get(url, params=params)
        return list(map(self.__map_recipe_option, response.json()["results"]))

    def get_recipe_information(self, option_id):
        url = f"{FOOD_API_URL}/recipes/{option_id}/information"
        params = {
            "apiKey": FOOD_API_KEY,
        }
        response = requests.get(url, params)
        print(response.json())
        return self.__map_recipe_information(response.json())

    def __map_recipe_option(self, option):
        return {
            "id": option["id"],
            "title": option["title"],
            "image": option["image"],
            "imageType": option["imageType"]
        }

    def __map_recipe_information(self, credentials):
        def map_ingredient(ingredient):
            return {
                'id': ingredient['id'],
                'nameClean': ingredient['nameClean'],
                'original': ingredient['original'],
                'measures': ingredient['measures']['us']
            }

        mapped_ingredients = list(map(map_ingredient, credentials["extendedIngredients"]))

        return {
            "ingredients": mapped_ingredients,
            "title": credentials["title"],
            "preparation_time": credentials["readyInMinutes"],
            "servings": credentials["servings"],
            "sourceUrl": credentials["sourceUrl"],
            "image": credentials["image"],
            "summary": credentials["summary"],
            "cuisines": credentials["cuisines"],
            "dishTypes": credentials["dishTypes"],
            "instructions": credentials["instructions"]
        }

