import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get("MONGO_URL")
FOOD_API_URL = os.environ.get("FOOD_API_URL")
FOOD_API_KEY = os.environ.get("FOOD_API_KEY")
