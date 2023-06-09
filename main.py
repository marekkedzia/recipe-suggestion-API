from fastapi import FastAPI
from recipe.recipe_controller import main as recipe_controller
from utils.health_controller import main as health_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_context():
    health_controller(app)
    controllers = [recipe_controller]
    for controller in controllers:
        app.include_router(controller())


load_context()
