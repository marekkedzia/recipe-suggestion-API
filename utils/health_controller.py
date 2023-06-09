from utils.database import get_database


def main(app):
    @app.get("/health")
    async def health():
        await get_database()
        return {"hello_there": "general_kenobi"}
