import motor.motor_asyncio

from utils.config_envs import MONGO_URL
from errors.errors import internal_server_error

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.lister


async def get_database():
    if not client:
        raise internal_server_error
    return db


async def get_recipe_collection():
    return db.recipe


async def get_file_metadata_collection():
    return db.metadata_collection
